# Figma-Defect-3.5K: A Neuro-Symbolic Cross-Modal Benchmark for UI Quality Assessment

> **Anonymous Repository for Double-Blind Peer Review**
> This repository contains the dataset, schemas, and evaluation scripts for the paper: *"Aligning Pixels and Nodes: A Neuro-Symbolic Cross-Modal Framework for Automated Web UI Quality Assessment"*.

## 📌 Introduction
Evaluating the structural integrity and visual fidelity of AI-generated web UIs remains a significant challenge due to the "semantic gap" between visual rendering (pixels) and structural logic (DOM nodes). 

**Figma-Defect-3.5K** is the first comprehensive benchmark designed for cross-modal UI defect detection. It contains 3,500 meticulously annotated UI components, featuring human-validated perturbations across multiple defect categories.

## 📊 Dataset Taxonomy
The dataset covers 5 primary UI defect categories commonly found in automated frontend generation:
1. **CSS Occlusion (30%)**: Elements overlapping incorrectly due to z-index or absolute positioning errors.
2. **Spatial Misalignment (25%)**: Flexbox/Grid alignment failures.
3. **Color Contrast Violation (20%)**: WCAG 2.1 accessibility failures.
4. **Text Overflow/Truncation (15%)**: Dynamic text breaking container boundaries.
5. **Missing/Broken Assets (10%)**: Unrendered icons or images.

## 📂 Data Structure
The dataset follows a dual-modality structure to support Neuro-Symbolic architectures (like our proposed CM-GAT):
- `images/`: High-resolution rendered UI screenshots (Pixels).
- `dom_trees/`: Parsed DOM hierarchies with CSS attributes (Nodes).
- `annotations.json`: Ground truth labels mapping bounding boxes to DOM XPaths, validated by 50 UX experts.

## 🚀 Quick Start

### Prerequisites

bash
pip install -r requirements.txt


### Loading the Dataset (PyTorch)
We provide a standard PyTorch `Dataset` class to easily load the multimodal data.

python
from scripts.datasetloader import FigmaDefectDataset
from torch.utils.data import DataLoader
Load the sample dataset
dataset = FigmaDefectDataset(annotationfile='dataset/sampledata/annotations.json')
dataloader = DataLoader(dataset, batchsize=16, shuffle=True)
for batch in dataloader:
images, domgraphs, labels = batch
Pass to CM-GAT or MLLM baselines


## ⚖️ Ethics and License
- **Ethics Approval:** All human evaluations (50 UX experts) were conducted with IRB approval. All participants provided informed consent.
- **License:** This dataset is released under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license for academic research purposes.

*(Note: The full 3.5K dataset will be publicly released upon manuscript acceptance. A representative sample is provided here for the peer-review process.)*


