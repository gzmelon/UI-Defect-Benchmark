"""
Q-Former Projection Layer
Projects graph-level representation into LLaMA-3 embedding space
as 32 learnable query tokens of width 768.
"""
import torch
import torch.nn as nn


class QFormerProjection(nn.Module):
    def __init__(self, graph_dim=768, llm_dim=4096, num_queries=32,
                 num_layers=6, hidden_dim=768, num_heads=8):
        super().__init__()
        self.queries = nn.Parameter(torch.randn(num_queries, hidden_dim) * 0.02)
        self.graph_proj = nn.Linear(graph_dim, hidden_dim)
        self.llm_proj = nn.Linear(hidden_dim, llm_dim)
        enc = nn.TransformerEncoderLayer(
            d_model=hidden_dim, nhead=num_heads,
            dim_feedforward=hidden_dim * 4, dropout=0.1, batch_first=True)
        self.transformer = nn.TransformerEncoder(enc, num_layers=num_layers)

    def forward(self, graph_embedding):
        B = graph_embedding.size(0)
        gf = self.graph_proj(graph_embedding).unsqueeze(1)
        q = self.queries.unsqueeze(0).expand(B, -1, -1) + gf
        return self.llm_proj(self.transformer(q))
