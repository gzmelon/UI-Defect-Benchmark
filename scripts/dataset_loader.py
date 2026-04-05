import json
import torch
from torch.utils.data import Dataset
from PIL import Image

class FigmaDefectDataset(Dataset):
    """
    PyTorch Dataset for loading Cross-Modal UI Data (Pixels + Nodes)
    """
    def __init__(self, annotation_file, transform=None):
        with open(annotation_file, 'r') as f:
            data = json.load(f)
        self.samples = data['samples']
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # 1. Load Sub-symbolic Pixels (Image)
        # image = Image.open(sample['image_path']).convert('RGB')
        # if self.transform: image = self.transform(image)
        
        # 2. Load Symbolic Nodes (Mocking Graph Data)
        node_features = sample['symbolic_nodes']['css_properties']
        
        # 3. Label
        label = torch.tensor(sample['defect_label'], dtype=torch.long)
        
        return {"image_path": sample['image_path'], "node_features": node_features}, label

if __name__ == "__main__":
    print("Dataset loader initialized successfully.")
