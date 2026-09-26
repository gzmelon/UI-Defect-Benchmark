# Model Card: NS-CQA

## Model Details

- **Name**: NS-CQA (Neuro-Symbolic Cross-modal Quality Assessment)
- **Version**: 1.0
- **Architecture**: RoBERTa-base + ViT-B/16 + CM-GAT (8 heads) +
  Q-Former + LLaMA-3-8B-Instruct (LoRA)
- **Parameters**: ~8.1B (full), 3.1B (distilled + INT8)
- **Input**: (rendered screenshot, serialized DOM, computed styles)
- **Output**: (defect type, severity, target node, repair suggestion)

## Intended Use

Automated quality assurance for AI-generated web UIs, suitable for
integration into CI/CD pipelines.

## Training Data

Figma-Defect-3.5K (3,500 samples). See `docs/data_card.md`.

## Training Procedure

- Symbolic encoder: RoBERTa-base, fine-tuned (lr = 1e-5)
- Visual encoder: ViT-B/16, frozen
- CM-GAT: 2 layers, 8 heads, hidden 768, dropout 0.1
- Q-Former: 32 queries, 6 layers, hidden 768
- LLM: LLaMA-3-8B-Instruct; LoRA r = 16, α = 32
- Optimizer: AdamW; weight decay 0.01; cosine schedule
- Hardware: 1 × NVIDIA A100 80GB
- Random seeds: 42, 123, 2024

## Evaluation

| Metric | NS-CQA | LLaVA-1.5 | LLaMA-3 concat |
|---|---|---|---|
| Precision | 92.1% | 86.5% | 84.9% |
| Recall | 90.8% | 85.2% | 83.6% |
| F1 | 0.914 | 0.858 | 0.842 |
| Accuracy | 91.5% | 85.9% | 84.2% |
| Specificity | 92.0% | 86.3% | 84.7% |
| AUC | 0.95 | 0.89 | 0.88 |
| Pearson r | 0.78 | 0.72 | – |

Effect size (vs. LLaVA-1.5): Cohen's d = 0.62; Cliff's delta = 0.47.

## Limitations

- Static DOM only; dynamic SPA states not handled (see Section 5.7).
- Large DOM trees (>5,000 nodes) require graph sparsification.
- Synthetic training data may not cover all real-world defect types.
- Mobile and mini-program pages only partially validated.

## Ethical Considerations

- IRB approval obtained from Guangzhou University of Software.
- All human annotators provided informed consent.
- No personally identifiable information collected.

## Environmental Impact

Training: approximately 72 GPU-hours on 1× NVIDIA A100 80GB.

## License

CC BY-NC-SA 4.0 for academic research.
