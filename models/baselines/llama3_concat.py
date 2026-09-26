"""
Fixed-Backbone LLaMA-3-8B Concatenation Baseline (CRITICAL COMPARISON)

This baseline receives NAIVE CONCATENATION of DOM text and screenshot
features, using the EXACT SAME training recipe as NS-CQA. The only
variable is whether CM-GAT is used for fusion.

This isolates the contribution of the neuro-symbolic graph attention
mechanism from the LLaMA-3-8B backbone itself, directly addressing
Reviewer #6's concern about baseline fairness.

Reference: Table 3, row 5 of the paper.
Expected performance: Precision 84.9%, Recall 83.6%, F1 0.842.
"""
from typing import Dict

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, CLIPVisionModel
    from peft import LoraConfig, get_peft_model
    import torch
    import torch.nn as nn
    from PIL import Image
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


class LLaMA3ConcatBaseline(nn.Module):
    def __init__(
        self,
        llm_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        vision_name: str = "openai/clip-vit-base-patch16",
        lora_r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.05,
        device: str = "cuda",
    ):
        super().__init__()
        if not HAS_DEPS:
            raise ImportError("Install transformers, peft, torch, Pillow.")
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(llm_name)
        llm = AutoModelForCausalLM.from_pretrained(
            llm_name, torch_dtype=torch.float16
        )
        lora_cfg = LoraConfig(
            r=lora_r, lora_alpha=lora_alpha, lora_dropout=lora_dropout,
            target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM",
        )
        self.llm = get_peft_model(llm, lora_cfg).to(device)
        self.vision_encoder = CLIPVisionModel.from_pretrained(vision_name).to(device)
        self.vision_proj = nn.Linear(768, 4096).to(device)  # CLIP → LLaMA
        self.classifier = nn.Linear(4096, 5).to(device)

    def forward(self, images, dom_texts):
        """
        Naive concatenation: project vision features to LLM space and
        prepend them to the DOM token embeddings.
        """
        pixel_values = torch.stack([self._to_tensor(img) for img in images]).to(self.device)
        vision_out = self.vision_encoder(pixel_values).last_hidden_state
        vision_feats = self.vision_proj(vision_out.mean(dim=1))  # [B, 4096]

        tokens = self.tokenizer(
            dom_texts, return_tensors="pt", padding=True, truncation=True,
            max_length=512,
        ).to(self.device)
        text_embeds = self.llm.get_input_embeddings()(tokens["input_ids"])
        # Naive concat: prepend vision feature as a single token
        combined = torch.cat([vision_feats.unsqueeze(1), text_embeds], dim=1)
        outputs = self.llm(inputs_embeds=combined, output_hidden_states=True)
        eos_hidden = outputs.hidden_states[-1][:, -1, :]
        return self.classifier(eos_hidden)

    def _to_tensor(self, image: Image.Image):
        import torchvision.transforms as T
        return T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ])(image)


if __name__ == "__main__":
    print("LLaMA-3-8B Concatenation Baseline (fixed-backbone).")
    print("This isolates CM-GAT contribution from the LLaMA-3 backbone.")
