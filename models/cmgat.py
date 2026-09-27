"""
Cross-Modal Graph Attention Network (CM-GAT)

An 8-head extension of the standard GAT adapted for cross-modal UI
graphs. The spatial edge MLP Φ(·) is shared across all heads.
"""
import torch
import torch.nn as nn


class CMGATLayer(nn.Module):
    def __init__(self, in_dim=768, out_dim=768, num_heads=8, dropout=0.1):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = out_dim // num_heads
        self.W = nn.Linear(in_dim, out_dim, bias=False)
        self.a = nn.Parameter(torch.zeros(num_heads, 2 * self.head_dim + 16))
        self.edge_mlp = nn.Sequential(
            nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 16))
        self.dropout = nn.Dropout(dropout)

    def forward(self, h, edge_index, edge_attr):
        N = h.size(0)
        Wh = self.W(h).view(N, self.num_heads, self.head_dim)
        src, dst = edge_index[0], edge_index[1]
        ef = self.edge_mlp(edge_attr).unsqueeze(1).expand(-1, self.num_heads, -1)
        concat = torch.cat([Wh[src], Wh[dst], ef], dim=-1)
        e = nn.functional.leaky_relu((concat * self.a.unsqueeze(0)).sum(-1), 0.2)
        e_max = torch.full((N, self.num_heads), -1e9, device=h.device)
        e_max.scatter_reduce_(0, dst.unsqueeze(1).expand(-1, self.num_heads),
                              e, reduce="amax", include_self=True)
        alpha = torch.exp(e - e_max[dst])
        denom = torch.zeros(N, self.num_heads, device=h.device)
        denom.index_add_(0, dst, alpha)
        alpha = alpha / (denom[dst] + 1e-9)
        out = torch.zeros(N, self.num_heads, self.head_dim, device=h.device)
        out.index_add_(0, dst, alpha.unsqueeze(-1) * Wh[src])
        return self.dropout(nn.functional.elu(out.reshape(N, -1)))


class CMGAT(nn.Module):
    def __init__(self, in_dim=768, hidden_dim=768, num_layers=2,
                 num_heads=8, dropout=0.1):
        super().__init__()
        self.layers = nn.ModuleList([
            CMGATLayer(in_dim if i == 0 else hidden_dim, hidden_dim,
                       num_heads, dropout) for i in range(num_layers)])

    def forward(self, h, edge_index, edge_attr):
        for layer in self.layers:
            h = layer(h, edge_index, edge_attr) + h
        return h
