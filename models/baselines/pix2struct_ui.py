"""
Pix2Struct Visual-Only Baseline
Fine-tuned Pix2Struct model for UI understanding.

This baseline receives ONLY the rendered screenshot (no DOM). It
demonstrates the ceiling of visual-only methods, which cannot localize
the responsible code node.

Reference: Table 3, row 2 of the paper.
Expected performance: Precision 74.3%, Recall 71.8%, F1 0.730.
"""
from typing import Dict, List

try:
    from transformers import Pix2StructForConditionalGeneration, Pix2StructProcessor
    import torch
    from PIL import Image
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


class Pix2StructUIBaseline:
    def __init__(self, model_name: str = "google/pix2struct-base", device: str = "cuda"):
        if not HAS_DEPS:
            raise ImportError("Install transformers, torch, and Pillow.")
        self.processor = Pix2StructProcessor.from_pretrained(model_name)
        self.model = Pix2StructForConditionalGeneration.from_pretrained(model_name).to(device)
        self.device = device

    def predict(self, image: Image.Image, prompt: str = "What UI defects are present?") -> str:
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=128)
        return self.processor.decode(outputs[0], skip_special_tokens=True)

    def evaluate(self, test_loader) -> Dict[str, float]:
        """Evaluate on the test split. Returns precision, recall, F1."""
        import numpy as np
        y_true, y_pred = [], []
        for image, _, label in test_loader:
            pred_text = self.predict(image)
            pred_defect = _parse_defect_from_text(pred_text)
            y_true.append(label["defect_type_id"])
            y_pred.append(pred_defect)
        return _compute_metrics(np.array(y_true), np.array(y_pred))


def _parse_defect_from_text(text: str) -> int:
    """Parse defect type from generated text. Maps to 0-4 index."""
    keywords = {
        0: ["occlusion", "overlap", "z-index"],
        1: ["misalign", "flex", "grid"],
        2: ["contrast", "color", "wcag"],
        3: ["overflow", "truncat", "text"],
        4: ["missing", "broken", "asset"],
    }
    text_lower = text.lower()
    for idx, kws in keywords.items():
        if any(kw in text_lower for kw in kws):
            return idx
    return -1


def _compute_metrics(y_true, y_pred) -> Dict[str, float]:
    from sklearn.metrics import precision_score, recall_score, f1_score
    return {
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


if __name__ == "__main__":
    print("Pix2Struct UI Baseline. See class docstring for usage.")
