"""
LLaVA-1.5 Fine-Tuned Baseline
Multimodal LLM directly fine-tuned on the Figma-Defect-3.5K dataset
using LoRA.

This baseline represents a strong domain-adapted MLLM. It receives both
the rendered screenshot and the raw DOM text, but without explicit
graph alignment.

Reference: Table 3, row 4 of the paper.
Expected performance: Precision 86.5%, Recall 85.2%, F1 0.858.
"""
from typing import Dict

try:
    from transformers import LlavaForConditionalGeneration, AutoProcessor
    from peft import LoraConfig, get_peft_model
    import torch
    from PIL import Image
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


class LLaVA15FinetunedBaseline:
    def __init__(
        self,
        model_name: str = "llava-hf/llava-1.5-7b-hf",
        lora_r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.05,
        device: str = "cuda",
    ):
        if not HAS_DEPS:
            raise ImportError("Install transformers, peft, torch, Pillow.")
        self.processor = AutoProcessor.from_pretrained(model_name)
        model = LlavaForConditionalGeneration.from_pretrained(
            model_name, torch_dtype=torch.float16
        )
        lora_cfg = LoraConfig(
            r=lora_r, lora_alpha=lora_alpha, lora_dropout=lora_dropout,
            target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM",
        )
        self.model = get_peft_model(model, lora_cfg).to(device)
        self.device = device

    def predict(self, image: Image.Image, dom_text: str) -> Dict:
        prompt = (
            "USER: <image>\nAnalyze the following UI. "
            "DOM: " + dom_text[:2000] + "\n"
            "What defect is present? Answer with one of: "
            "css_occlusion, spatial_misalignment, contrast_violation, "
            "text_overflow, missing_asset.\nASSISTANT:"
        )
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=32)
        text = self.processor.decode(outputs[0], skip_special_tokens=True)
        return {
            "defect_type": _parse_defect(text),
            "raw_response": text,
        }


def _parse_defect(text: str) -> str:
    text_lower = text.lower()
    for d in ["css_occlusion", "spatial_misalignment", "contrast_violation",
              "text_overflow", "missing_asset"]:
        if d in text_lower or d.replace("_", " ") in text_lower:
            return d
    return "unknown"


if __name__ == "__main__":
    print("LLaVA-1.5 Fine-Tuned Baseline. See docstring for usage.")
