import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool

class CrossModalGAT(nn.Module):
    """
    Cross-Modal Graph Attention Network (CM-GAT)
    Proposed in: "Aligning Pixels and Nodes: A Neuro-Symbolic Cross-Modal Framework..."
    
    This module fuses sub-symbolic visual features (from rendered UI pixels) 
    with symbolic structural features (from DOM tree graphs).
    """
    def __init__(self, visual_dim=768, node_dim=256, hidden_dim=512, num_classes=5):
        super(CrossModalGAT, self).__init__()
        
        # 1. Visual Pathway (Projects ViT features)
        self.visual_proj = nn.Sequential(
            nn.Linear(visual_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU()
        )

        # 2. Symbolic Graph Pathway (Processes DOM Tree using Graph Attention)
        self.node_proj = nn.Linear(node_dim, hidden_dim)
        # Multi-head GAT layers for structural message passing
        self.gat1 = GATConv(hidden_dim, hidden_dim // 2, heads=4, concat=True, dropout=0.2)
        self.gat2 = GATConv(hidden_dim * 2, hidden_dim, heads=1, concat=False, dropout=0.2)

        # 3. Cross-Modal Fusion Module
        self.fusion_layer = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Dropout(0.3)
        )

        # 4. Assessment Head (Defect Classification)
        self.classifier = nn.Linear(hidden_dim, num_classes)

    def forward(self, visual_features, node_features, edge_index, batch):
        """
        Args:
            visual_features: Tensor [Batch, visual_dim] from ViT/CNN
            node_features: Tensor [Num_nodes, node_dim] from DOM CSS/HTML properties
            edge_index: Tensor [2, Num_edges] representing DOM parent-child links
            batch: Tensor mapping nodes to their respective graphs in the batch
        """
        # Step 1: Extract Visual Embeddings
        v_feat = self.visual_proj(visual_features) # [Batch, Hidden]

        # Step 2: Extract Symbolic Graph Embeddings
        x = F.elu(self.node_proj(node_features))
        x = F.elu(self.gat1(x, edge_index))
        x = self.gat2(x, edge_index)
        
        # Pool node-level features into a single graph-level representation
        g_feat = global_mean_pool(x, batch) # [Batch, Hidden]

        # Step 3: Neuro-Symbolic Alignment & Fusion
        # Concatenate aligned visual and structural features
        fused_feat = torch.cat([v_feat, g_feat], dim=-1)
        fused_feat = self.fusion_layer(fused_feat)

        # Step 4: Quality Assessment Prediction
        logits = self.classifier(fused_feat)
        
        return logits

if __name__ == "__main__":
    # Dummy test to ensure model compiles and prints parameters
    model = CrossModalGAT()
    print("CM-GAT Architecture Initialized Successfully.")
    print(f"Total Trainable Parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
