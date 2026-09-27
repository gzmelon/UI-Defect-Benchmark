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
