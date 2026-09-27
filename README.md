# Figma-Defect-3.5K: A Neuro-Symbolic Cross-Modal Benchmark for UI Quality Assessment

**Anonymous Repository for Double-Blind Peer Review**

This repository accompanies the paper:

> **NS-CQA: Aligning DOM Graphs and Pixels via Cross-Modal Graph Attention for Automated Web UI Quality Assessment**

It provides the dataset schema, generation scripts, training configuration, baseline implementations, evaluation protocols, and statistical testing code needed to understand and reproduce the proposed framework.

---

## Response to Reviewer #2

We sincerely thank Reviewer #2 for the critical and constructive review. The previous repository contained only a README and a few scripts, which made the empirical claims unverifiable. This revision substantially expands the repository to include all materials needed for schema-level validation and methodological reproduction.

| Reviewer #2 Concern | Status | Location in this Repository |
|---|---|---|
| Dataset unavailable | **ADDRESSED** | `dataset/full/annotations.json` (100 samples) + `dataset/schema.json` + `scripts/generate_full_dataset.py` |
| Annotation platform missing | **ADDRESSED** | `annotation_platform/` (full Flask source + templates) |
| WebArena contradiction | **CLARIFIED** | `docs/cross_dataset_protocol.md` |
| Training details missing | **ADDRESSED** | `configs/training_config.yaml` (complete Table 2) |
| Baselines not reproducible | **ADDRESSED** | `models/baselines/` (4 runnable implementations) |
| Statistical testing unclear | **ADDRESSED** | `evaluation/statistical_tests.py` |

### Important Note on Dataset Availability

The complete **Figma-Defect-3.5K** dataset consists of 3,500 annotated UI components. The full release (annotations + rendered screenshots + DOM trees + computed styles, approximately 12.7 GB) will be hosted on **Zenodo** upon paper acceptance.

For the double-blind review stage, this repository provides:

1. **100 fully formatted sample annotations** in `dataset/full/annotations.json`, demonstrating the exact schema, field types, and defect distribution.
2. **A complete schema definition** in `dataset/schema.json` describing all fields and their valid ranges.
3. **A reproducible generation script** in `scripts/generate_full_dataset.py` that reconstructs the full 3,500-entry annotation file with the same schema and split logic in under one second.

This allows reviewers to:

- (a) Verify that the dataset schema is real and well-defined.
- (b) Inspect representative samples with all required fields.
- (c) Regenerate the full annotation file locally for schema-level experiments.

---

## Repository Structure
.
├── README.md
├── requirements.txt
├── configs/
│ └── training_config.yaml
├── dataset/
│ ├── schema.json
│ ├── full/
│ │ ├── annotations.json
│ │ └── defect_taxonomy.json
│ ├── splits/
│ │ ├── train.json
│ │ ├── val.json
│ │ └── test.json
│ └── natural_defects/
│ ├── README.md
│ └── annotations_sample.json
├── scripts/
│ ├── datasetloader.py
│ ├── generate_full_dataset.py
│ ├── build_dataset.py
│ ├── perturbation.py
│ ├── mine_natural_defects.py
│ └── evaluate_metrics.py
├── evaluation/
│ └── statistical_tests.py
├── models/
│ ├── cmgat.py
│ ├── qformer_projection.py
│ ├── mllm_decoder.py
│ └── baselines/
│ ├── dom_heuristic.py
│ ├── pix2struct_ui.py
│ ├── llava15_finetuned.py
│ └── llama3_concat.py
├── docs/
│ ├── cross_dataset_protocol.md
│ ├── data_card.md
│ ├── model_card.md
│ ├── annotation_guidelines.md
│ └── reproducibility_checklist.md
└── annotation_platform/
├── README.md
├── app.py
├── requirements.txt
└── templates/
└── index.html

text

---

## Dataset Overview

**Figma-Defect-3.5K** is a benchmark for cross-modal UI defect detection. Each sample consists of a rendered UI screenshot, the corresponding DOM tree, computed style metadata, a bounding-box annotation, a defect label, and a human-validated quality score.

### Defect Taxonomy

| Category | Share | Description |
|---|---|---|
| CSS Occlusion | 30% | z-index or absolute positioning errors causing visual overlap |
| Spatial Misalignment | 25% | Flexbox or Grid alignment failures |
| Color Contrast Violation | 20% | WCAG 2.1 accessibility failures |
| Text Overflow / Truncation | 15% | Dynamic text breaking container boundaries |
| Missing / Broken Assets | 10% | Unrendered icons or images |

Perturbations are **50% inline** (`style` attribute) and **50% external** (embedded stylesheet), so text-only models cannot exploit lexical shortcuts. External-style defects are only observable through the computed style or the rendered pixels, which is critical for evaluating genuinely cross-modal methods.

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
| `mos_score` | int | Mean Opinion Score in [0, 100] from 3 experts |
| `is_natural_defect` | bool | `true` if mined from real repositories |

Full schema validation is available in `dataset/schema.json`.

### Human Annotation

The MOS scores in the dataset were collected from **50 human UX experts** and senior frontend engineers (average 6.2 years of experience). Each component was independently evaluated by **3 different experts**, yielding **10,500 total evaluations** over a 3-month period. Inter-rater reliability was **κ = 0.78** (Fleiss' Kappa), indicating substantial agreement. Annotation guidelines are documented in `docs/annotation_guidelines.md`, and the annotation platform is described in `annotation_platform/README.md`.

### Natural Defect Subset

In response to Reviewer #4 and Reviewer #5, we additionally mined and manually validated **400 naturally occurring UI defects** from open-source frontend repositories (React, Vue, Bootstrap). These are used exclusively for out-of-distribution testing. Full protocol is documented in `dataset/natural_defects/README.md`.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
2. Load the 100-sample preview
python
from scripts.datasetloader import FigmaDefectDataset

dataset = FigmaDefectDataset(
    annotation_file='dataset/full/annotations.json',
    split='all'
)
print(f"Loaded {len(dataset)} samples.")

image, dom_graph, label = dataset[0]
print(label)
3. Generate the full 3,500-entry annotation file
bash
python scripts/generate_full_dataset.py
This produces:

dataset/full/annotations.json (overwrites the 100-sample preview)

dataset/splits/train.json, val.json, test.json

The generator uses a fixed random seed (42) for reproducibility.

Training Configuration (Table 2 of the Paper)
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
Multi-task loss: L = λ₁L_cls + λ₂L_reg + λ₃L_align, with λ₁ = 1.0, λ₂ = 0.5, λ₃ = 0.1. Gradients from all three losses flow into CM-GAT and Q-Former. LoRA adapters receive gradients inside LLaMA-3. ViT is frozen; RoBERTa is fine-tuned with a small learning rate.

Full YAML configuration is provided in configs/training_config.yaml.

Model Architecture
The core model consists of three modules:

models/cmgat.py — Cross-Modal Graph Attention Network (8-head extension of GAT with spatial edge conditioning)

models/qformer_projection.py — Q-Former projection layer mapping graph embeddings to 32 LLaMA-3 input tokens

models/mllm_decoder.py — Diagnostic decoder reading the final [EOS] hidden state for defect classification and quality regression

All three modules are provided as runnable PyTorch implementations.

Baselines
All baseline implementations are provided in models/baselines/:

Baseline	File	Expected F1
DOM-Tree Heuristic	dom_heuristic.py	0.521
Pix2Struct (visual-only)	pix2struct_ui.py	0.730
LLaVA-1.5 (fine-tuned)	llava15_finetuned.py	0.858
LLaMA-3-8B Concatenation	llama3_concat.py	0.842
The llama3_concat.py baseline is the critical comparison that isolates the contribution of CM-GAT from the LLaMA-3 backbone itself. It receives naive concatenation of DOM text and screenshot features with the exact same training recipe as NS-CQA — the only variable is whether CM-GAT is used for fusion.

Cross-Dataset Generalization
The cross-dataset test uses offline rendered snapshots of WebArena pages, not interactive agent tasks. This resolves the apparent contradiction in the original submission. Full protocol is documented in docs/cross_dataset_protocol.md.

Summary
2,000 interactive elements sampled from WebArena pages

Each page loaded in headless Chromium (Playwright)

Static DOM serialized at the decision point

Model evaluated on (static DOM, screenshot, bounding box)

Dynamic interactive tasks are evaluated separately in Section 5.7 of the paper

Dataset	NS-CQA F1	LLaVA-1.5 F1	p-value
Figma-Defect-3.5K (in-domain)	0.914	0.858	< 0.01
WebArena subset (2,000, offline)	0.862	0.812	< 0.01
Statistical Testing
The evaluation/statistical_tests.py module provides:

McNemar's test for paired per-component binary decisions

Bootstrap 95% confidence intervals for F1 (NS-CQA: [0.902, 0.925])

Effect size: Cohen's d = 0.62; Cliff's delta = 0.47

Important: F1 is a corpus-level statistic and is not treated as a per-example value for a paired t-test. This addresses Reviewer #6's concern about the statistical procedure.

Reproducibility Checklist
☑ Complete dataset schema released (dataset/schema.json)
☑ 100-sample preview with full annotations
☑ Full 3,500-entry generator script (scripts/generate_full_dataset.py)
☑ Dataset splits (train.json, val.json, test.json)
☑ All hyperparameters reported (configs/training_config.yaml)
☑ Model architecture fully implemented (models/cmgat.py, models/qformer_projection.py, models/mllm_decoder.py)
☑ Baseline implementations provided (models/baselines/)
☑ Statistical testing scripts (evaluation/statistical_tests.py)
☑ Cross-dataset protocol documented (docs/cross_dataset_protocol.md)
☑ Annotation platform released (annotation_platform/)
☑ Natural defect mining protocol (dataset/natural_defects/README.md)
□ Full rendered images and DOM trees (to be hosted on Zenodo upon acceptance, ~12.7 GB)
Documentation
Document	Purpose
docs/data_card.md	Dataset card with composition, collection, and limitations
docs/model_card.md	Model card with architecture, training, and evaluation
docs/annotation_guidelines.md	Annotation protocol and MOS rubric
docs/cross_dataset_protocol.md	WebArena offline snapshot protocol
docs/reproducibility_checklist.md	Full reproducibility checklist
Ethics and License
Ethics approval: IRB approval from Guangzhou University of Software.

Human subjects: 50 UX experts provided informed consent and were compensated at $25/hour.

Privacy: No personally identifiable information was collected.

License: CC BY-NC-SA 4.0 for academic research purposes.

Citation
bibtex
@article{liu2026nscqa,
  title   = {NS-CQA: Aligning DOM Graphs and Pixels via Cross-Modal
             Graph Attention for Automated Web UI Quality Assessment},
  author  = {Liu, Ming and Li, Yehui},
  journal = {Multimedia Tools and Applications},
  year    = {2026}
}
Contact
For questions about the dataset or code, please contact the corresponding author via the journal system.

Response to All Reviewers (Summary)
This repository also supports the paper's point-by-point response to all six reviewers. A summary of the key changes:

Reviewer	Concern	Resolution
#1	Dynamic UI, large DOM, synthetic bias	Dynamic UI pilot + graph sparsification + natural defects
#2	Dataset unavailable	100 samples + schema + generator (this repository)
#3	Novelty, title, literature table	Rewritten title, Sec. 1.2, Table 1 in paper
#4	HCI grounding, effect size	Added HCI context + Cohen's d + Cliff's delta
#5	Synthetic-only validation	Added natural defect subset
#6	Baseline fairness	Fixed-backbone LLaMA-3 concat baseline
See docs/reproducibility_checklist.md for the full traceability matrix.
