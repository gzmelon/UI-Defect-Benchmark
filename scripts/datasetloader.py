"""
Figma-Defect-3.5K Dataset Loader
"""
import json
from pathlib import Path
from typing import Optional, Literal
import torch
from torch.utils.data import Dataset
from PIL import Image

DEFECT_TYPES = [
    "css_occlusion", "spatial_misalignment", "contrast_violation",
    "text_overflow", "missing_asset"
]
SEVERITY_MAP = {"critical": 3, "major": 2, "minor": 1}

class FigmaDefectDataset(Dataset):
    def __init__(self, annotation_file, image_dir=None, dom_dir=None,
                 split: Literal["train","val","test","all"]="all", transform=None):
        self.annotation_file = Path(annotation_file)
        self.image_dir = Path(image_dir) if image_dir else self.annotation_file.parent / "images"
        self.dom_dir = Path(dom_dir) if dom_dir else self.annotation_file.parent / "dom_trees"
        self.transform = transform
        with open(self.annotation_file) as f:
            self.annotations = json.load(f)
        if split != "all":
            split_file = self.annotation_file.parent.parent / "splits" / f"{split}.json"
            with open(split_file) as f:
                split_ids = set(json.load(f)["image_ids"])
            self.annotations = [a for a in self.annotations if a["image_id"] in split_ids]
        if not self.annotations:
            raise ValueError(f"No annotations for split={split}")

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        ann = self.annotations[idx]
        img_path = self.image_dir / f"{ann['image_id']}.png"
        if not img_path.exists():
            img_path = self.image_dir / f"{ann['image_id']}.jpg"
        image = Image.open(img_path).convert("RGB")
        bbox = ann["bounding_box"]
        image = image.crop((bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]))
        if self.transform:
            image = self.transform(image)
        dom_path = self.dom_dir / f"{ann['image_id']}.json"
        dom_data = json.load(open(dom_path)) if dom_path.exists() else {"nodes":[], "edges":[]}
        label = {
            "defect_type": ann["defect_type"],
            "defect_type_id": DEFECT_TYPES.index(ann["defect_type"]) if ann["defect_type"] in DEFECT_TYPES else -1,
            "severity": SEVERITY_MAP.get(ann.get("severity","minor"), 1),
            "mos_score": ann.get("mos_score", 50.0)/100.0,
            "repair_suggestion": ann.get("repair_suggestion",""),
            "injection_method": ann.get("injection_method","unknown"),
            "is_natural_defect": ann.get("is_natural_defect", False),
        }
        return image, dom_data, label
