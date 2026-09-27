"""
MLLM Diagnostic Decoder
Reads final [EOS] hidden state from LLaMA-3 and produces
defect-type logits and quality score Q̂ ∈ [0, 1].
"""
import torch
import torch.nn as nn


class DiagnosticDecoder(nn.Module):
    def __init__(self, llm_dim=4096, num_defect_types=5):
        super().__init__()
        self.classifier = nn.Linear(llm_dim, num_defect_types)
        self.regressor = nn.Sequential(
            nn.Linear(llm_dim, 512), nn.ReLU(),
            nn.Linear(512, 1), nn.Sigmoid())

    def forward(self, eos_hidden):
        return self.classifier(eos_hidden), self.regressor(eos_hidden)


def multi_task_loss(logits, score, target_type, target_score,
                    lambda_cls=1.0, lambda_reg=0.5, lambda_align=0.1):
    L_cls = nn.functional.cross_entropy(logits, target_type)
    L_reg = nn.functional.mse_loss(score.squeeze(-1), target_score)
    L_align = torch.zeros_like(L_cls)
    return lambda_cls * L_cls + lambda_reg * L_reg + lambda_align * L_align
