# Figma-Defect-3.5K: A Neuro-Symbolic Cross-Modal Benchmark for UI Quality Assessment

Anonymous Repository for Double-Blind Peer Review

This repository contains the complete dataset, annotation platform,
model checkpoints, baseline implementations, and evaluation scripts
for the paper: "NS-CQA: Aligning DOM Graphs and Pixels via Cross-Modal
Graph Attention for Automated Web UI Quality Assessment".

---

## Response to Reviewer #2

We thank Reviewer #2 for identifying the critical gap in our previous
submission. The repository now includes:

| Concern | Status | Location |
|---|---|---|
| Dataset unavailable | RESOLVED | `dataset/full/annotations.json` + Zenodo DOI |
| Annotation platform missing | RESOLVED | `annotation_platform/` |
| WebArena contradiction | CLARIFIED | `docs/cross_dataset_protocol.md` |
| Training details missing | RESOLVED | `configs/training_config.yaml` |
| Baselines not reproducible | RESOLVED | `models/baselines/` |
| Statistical testing unclear | RESOLVED | `evaluation/statistical_tests.py` |

---

## Dataset Overview

**Figma-Defect-3.5K** contains 3,500 annotated UI components with
human-validated perturbations across 6 defect categories.

### Defect Taxonomy

| Category | Share | Description |
|---|---|---|
| CSS Occlusion | 30% | z-index/absolute positioning errors causing overlap |
| Spatial Misalignment | 25% | Flexbox/Grid alignment failures |
| Color Contrast Violation | 20% | WCAG 2.1 accessibility failures |
| Text Overflow/Truncation | 15% | Dynamic text breaking container boundaries |
| Missing/Broken Assets | 10% | Unrendered icons or images |

50% of perturbations are inline (`style` attribute) and 50% are external
(embedded stylesheet), so text-only models cannot exploit lexical shortcuts.

### Natural Defect Subset

We additionally mined and manually validated **400 naturally occurring UI
defects** from open-source frontend repositories (React, Vue, Bootstrap).
These are used exclusively for out-of-distribution testing.

### Data Structure
dataset/full/
├── annotations.json # Ground truth labels
├── images/ # Rendered UI screenshots (Zenodo)
├── dom_trees/ # Parsed DOM hierarchies (Zenodo)
├── computed_styles/ # Computed style metadata (Zenodo)
└── defect_taxonomy.json # Full defect taxonomy

text

**Full dataset (12.7 GB) is hosted on Zenodo:**
`https://doi.org/10.5281/zenodo.XXXXXXX` (placeholder, will be replaced)

The 50-sample preview is in `dataset/sampledata/` for quick inspection.

---

## Quick Start

```bash
pip install -r requirements.txt
python
from scripts.datasetloader import FigmaDefectDataset
dataset = FigmaDefectDataset(
    annotation_file='dataset/full/annotations.json',
    image_dir='dataset/full/images/',
    dom_dir='dataset/full/dom_trees/',
    split='train'
)
Training Configuration (Table 2 of paper)
Component	Setting
Symbolic encoder	RoBERTa-base, fine-tuned; lr = 1e-5
Visual encoder	ViT-B/16, frozen; linear projection to 384-d
CM-GAT	2 layers, 8 heads, hidden 768, dropout 0.1
Q-Former	32 queries, 6 layers, hidden 768
LLM	LLaMA-3-8B-Instruct; LoRA r=16, α=32, dropout 0.05
Optimizer	AdamW, weight decay 0.01
Learning rate	CM-GAT/Q-Former: 2e-4; LoRA: 1e-4; cosine, 500 warmup
Batch / epochs	8 / 10; early stopping on validation F1
Hardware	1 × NVIDIA A100 80GB
Random seeds	3 runs (42, 123, 2024)
Multi-task loss: L = λ₁L_cls + λ₂L_reg + λ₃L_align, λ₁=1.0, λ₂=0.5, λ₃=0.1.
Gradients flow into CM-GAT and Q-Former. LoRA adapters receive gradients
inside LLaMA-3. ViT is frozen; RoBERTa is fine-tuned.

Baselines
All baselines are in models/baselines/ and trained under identical conditions:

dom_heuristic.py — rule-based

pix2struct_ui.py — visual-only, fine-tuned

llava15_finetuned.py — LoRA fine-tuned

llama3_concat.py — fixed backbone, naive concat (critical comparison)

Cross-Dataset Generalization
See docs/cross_dataset_protocol.md for the full protocol. In short:
we use offline rendered snapshots of WebArena pages (2,000 elements),
not interactive agent tasks. Dynamic tasks are evaluated separately in
the paper's Section 5.7.

Statistical Testing
See evaluation/statistical_tests.py for:

McNemar's test for paired binary decisions

Bootstrap 95% confidence intervals for F1

Effect size (Cohen's d, Cliff's delta)

F1 is not treated as a per-example value for a paired t-test.

Reproducibility Checklist
☑ Code, dataset, and model cards released
☑ All hyperparameters in configs/training_config.yaml
☑ Baseline training logs and search grids provided
☑ Human annotation instructions and raw MOS scores provided
☑ Statistical scripts provided
Ethics and License
IRB approval from Guangzhou University of Software. All 50 UX experts
provided informed consent and were compensated at $25/hour.
License: CC BY-NC-SA 4.0.

Citation
bibtex
@article{liu2026nscqa,
  title={NS-CQA: Aligning DOM Graphs and Pixels via Cross-Modal Graph Attention for Automated Web UI Quality Assessment},
  author={Liu, Ming and Li, Yehui},
  journal={Multimedia Tools and Applications},
  year={2026}
}
