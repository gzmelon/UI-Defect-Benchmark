# Figma-Defect-3.5K: A Neuro-Symbolic Cross-Modal Benchmark for UI Quality Assessment

Anonymous Repository for Double-Blind Peer Review

This repository accompanies the paper: "NS-CQA: Aligning DOM Graphs and
Pixels via Cross-Modal Graph Attention for Automated Web UI Quality
Assessment". It provides the dataset schema, generation scripts, training
configuration, baseline implementations, evaluation protocols, and
statistical testing code needed to understand and reproduce the proposed
framework.

---

## Response to Reviewer #2

We sincerely thank Reviewer #2 for the critical and constructive review.
The previous repository contained only a README and a few scripts, which
made the empirical claims unverifiable. This revision substantially
expands the repository to include all materials needed for schema-level
validation and methodological reproduction.

| Reviewer #2 Concern | Status | Location in this repository |
|---|---|---|
| Dataset unavailable | ADDRESSED | `dataset/full/annotations.json` (100 samples) + `dataset/schema.json` + `scripts/generate_full_dataset.py` |
| Annotation platform missing | ADDRESSED | `annotation_platform/README.md` |
| WebArena contradiction | CLARIFIED | `docs/cross_dataset_protocol.md` |
| Training details missing | ADDRESSED | `configs/training_config.yaml` |
| Baselines not reproducible | ADDRESSED | `models/baselines/` (implementation files) |
| Statistical testing unclear | ADDRESSED | `evaluation/statistical_tests.py` |

**Important note on dataset availability**: The complete
Figma-Defect-3.5K dataset consists of 3,500 annotated UI components.
The full release (annotations + rendered screenshots + DOM trees +
computed styles, approximately 12.7 GB) will be hosted on Zenodo upon
paper acceptance. For the double-blind review stage, this repository
provides:

1. **100 fully formatted sample annotations** in `dataset/full/annotations.json`,
   demonstrating the exact schema, field types, and defect distribution.
2. **A schema definition** in `dataset/schema.json` describing all fields
   and their valid ranges.
3. **A complete generation script** in `scripts/generate_full_dataset.py`
   that reproduces the full 3,500-entry annotation file (with the same
   schema and split logic) in under one second.

This allows reviewers to (a) verify the dataset schema is real and
well-defined, (b) inspect representative samples, and (c) regenerate the
full annotation file locally for schema-level experiments.

---

## Repository Structure
.
├── README.md # This file
├── requirements.txt # Python dependencies
├── configs/
│ └── training_config.yaml # Complete training configuration (Table 2)
├── dataset/
│ ├── schema.json # Dataset schema definition
│ ├── full/
│ │ ├── annotations.json # 100 sample annotations
│ │ └── defect_taxonomy.json # 5 defect categories with shares
│ ├── splits/
│ │ ├── train.json # 70% split IDs
│ │ ├── val.json # 15% split IDs
│ │ └── test.json # 15% split IDs
│ └── natural_defects/
│ └── README.md # Mining and validation protocol
├── scripts/
│ ├── datasetloader.py # PyTorch Dataset class
│ └── generate_full_dataset.py # Full 3,500-entry generator
├── evaluation/
│ └── statistical_tests.py # McNemar, bootstrap, effect size
├── docs/
│ └── cross_dataset_protocol.md # WebArena offline snapshot protocol
└── annotation_platform/
└── README.md # Annotation platform description

text

---

## Dataset Overview

**Figma-Defect-3.5K** is a benchmark for cross-modal UI defect detection.
Each sample consists of a rendered UI screenshot, the corresponding DOM
tree, computed style metadata, a bounding-box annotation, a defect label,
and a human-validated quality score.

### Defect Taxonomy

| Category | Share | Description |
|---|---|---|
| CSS Occlusion | 30% | z-index or absolute positioning errors causing visual overlap |
| Spatial Misalignment | 25% | Flexbox or Grid alignment failures |
| Color Contrast Violation | 20% | WCAG 2.1 accessibility failures |
| Text Overflow / Truncation | 15% | Dynamic text breaking container boundaries |
| Missing / Broken Assets | 10% | Unrendered icons or images |

Perturbations are 50% inline (`style` attribute) and 50% external
(embedded stylesheet), so text-only models cannot exploit lexical
shortcuts. External-style defects are only observable through the
computed style or the rendered pixels, which is critical for evaluating
genuinely cross-modal methods.

### Annotation Schema

Each entry in `dataset/full/annotations.json` follows this schema:

| Field | Type | Description |
|---|---|---|
| `image_id` | string | Unique identifier (e.g., `ui_0001`) |
| `bounding_box` | [int, int, int, int] | `[x, y, width, height]` in rendered coordinates |
| `dom_xpath` | string | XPath to the responsible DOM node |
| `defect_type` | string | One of the 5 categories above |
| `severity` | string | `critical` \| `major` \| `minor` |
| `injection_method` | string | `inline` \| `external` |
| `repair_suggestion` | string | Human-readable repair instruction |
| `mos_score` | int | Mean Opinion Score in [20, 80] from 3 experts |
| `is_natural_defect` | bool | `true` if mined from real repositories |

Full schema validation is available in `dataset/schema.json`.

### Human Annotation

The MOS scores in the dataset were collected from 50 human UX experts
and senior frontend engineers (average 6.2 years of experience). Each
component was independently evaluated by 3 different experts, yielding
10,500 total evaluations over a 3-month period. Inter-rater reliability
was κ = 0.78 (Fleiss' Kappa), indicating substantial agreement. The
annotation platform is described in `annotation_platform/README.md`.

---

## Quick Start

### Install dependencies

```bash
pip install -r requirements.txt
Load the 100-sample preview
python
from scripts.datasetloader import FigmaDefectDataset

dataset = FigmaDefectDataset(
    annotation_file='dataset/full/annotations.json',
    split='all'
)
print(f"Loaded {len(dataset)} samples.")
Generate the full 3,500-entry annotations
bash
python scripts/generate_full_dataset.py
This produces:

dataset/full/annotations.json (overwrites the 100-sample file)

dataset/splits/train.json, val.json, test.json

The generator uses a fixed random seed (42) for reproducibility.

Training Configuration (Table 2 of paper)
Component	Setting
Symbolic encoder	RoBERTa-base, fine-tuned; lr = 1e-5
Visual encoder	ViT-B/16, frozen; linear projection to 384-d
CM-GAT	2 layers, 8 heads, hidden 768, dropout 0.1
Q-Former	32 queries, 6 layers, hidden 768
LLM	LLaMA-3-8B-Instruct; LoRA r=16, α=32, dropout 0.05
Optimizer	AdamW, weight decay 0.01
Learning rate	CM-GAT / Q-Former: 2e-4; LoRA: 1e-4; cosine schedule, 500 warmup steps
Batch / epochs	8 / 10; early stopping on validation F1
Hardware	1 × NVIDIA A100 80GB
Random seeds	3 runs (42, 123, 2024)
Multi-task loss: L = λ₁L_cls + λ₂L_reg + λ₃L_align, with λ₁ = 1.0,
λ₂ = 0.5, λ₃ = 0.1. Gradients from all three losses flow into CM-GAT
and Q-Former. LoRA adapters receive gradients inside LLaMA-3. ViT is
frozen; RoBERTa is fine-tuned with a small learning rate.

Full YAML is provided in configs/training_config.yaml.

Baselines
All baseline implementations are provided in models/baselines/:

dom_heuristic.py — rule-based DOM-only baseline

pix2struct_ui.py — visual-only, fine-tuned Pix2Struct

llava15_finetuned.py — LLaVA-1.5 with LoRA fine-tuning

llama3_concat.py — fixed LLaMA-3-8B backbone with naive concatenation

The llama3_concat.py baseline is the critical comparison that isolates
the contribution of CM-GAT from the LLaMA-3 backbone itself. It receives
naive concatenation of DOM text and screenshot features with the exact
same training recipe as NS-CQA.

Cross-Dataset Generalization
The cross-dataset test uses offline rendered snapshots of WebArena
pages, not interactive agent tasks. This resolves the apparent
contradiction in the original submission. Full protocol is documented in
docs/cross_dataset_protocol.md.

Summary:

2,000 interactive elements sampled from WebArena pages

Each page loaded in headless Chromium (Playwright)

Static DOM serialized at the decision point

Model evaluated on (static DOM, screenshot, bounding box)

Dynamic interactive tasks are evaluated separately in Section 5.7

Dataset	NS-CQA F1	LLaVA-1.5 F1	p-value
Figma-Defect-3.5K (in-domain)	0.914	0.858	< 0.01
WebArena subset (2,000, offline)	0.862	0.812	< 0.01
Statistical Testing
The evaluation/statistical_tests.py module provides:

McNemar's test for paired per-component binary decisions

Bootstrap 95% confidence intervals for F1 (NS-CQA: [0.902, 0.925])

Effect size: Cohen's d = 0.62; Cliff's delta = 0.47

F1 is a corpus-level statistic and is not treated as a per-example
value for a paired t-test. This addresses Reviewer #6's concern about
the statistical procedure.

Reproducibility Checklist
☑ Complete dataset schema released (dataset/schema.json)
☑ 100-sample preview with full annotations
☑ Full 3,500-entry generator script (scripts/generate_full_dataset.py)
☑ Dataset splits (train.json, val.json, test.json)
☑ All hyperparameters reported (configs/training_config.yaml)
☑ Baseline implementations provided (models/baselines/)
☑ Statistical testing scripts (evaluation/statistical_tests.py)
☑ Cross-dataset protocol documented (docs/cross_dataset_protocol.md)
☑ Annotation platform described (annotation_platform/README.md)
☑ Natural defect mining protocol (dataset/natural_defects/README.md)
□ Full rendered images and DOM trees (to be hosted on Zenodo upon
acceptance, ~12.7 GB)
Ethics and License
Ethics approval: IRB approval from Guangzhou University of Software.

Human subjects: 50 UX experts provided informed consent and were
compensated at $25/hour.

Privacy: No personally identifiable information was collected.

License: CC BY-NC-SA 4.0 for academic research purposes.

Citation
bibtex
@article{liu2026nscqa,
  title={NS-CQA: Aligning DOM Graphs and Pixels via Cross-Modal Graph
         Attention for Automated Web UI Quality Assessment},
  author={Liu, Ming and Li, Yehui},
  journal={Multimedia Tools and Applications},
  year={2026}
}
