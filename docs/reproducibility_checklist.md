# Reproducibility Checklist

## Dataset

- [x] Dataset schema documented (`dataset/schema.json`)
- [x] Sample annotations released (100 entries in `dataset/full/`)
- [x] Full annotation generator released (`scripts/generate_full_dataset.py`)
- [x] Data splits provided (`dataset/splits/train.json`, `val.json`, `test.json`)
- [ ] Full rendered screenshots and DOM trees (~12.7 GB) — pending Zenodo
  hosting upon paper acceptance
- [x] Natural defect mining protocol documented
- [x] Annotation guidelines released (`docs/annotation_guidelines.md`)

## Code

- [x] All model components implemented (`models/`)
- [x] All baseline implementations released (`models/baselines/`)
- [x] Data loader released (`scripts/datasetloader.py`)
- [x] Dataset builder released (`scripts/build_dataset.py`)
- [x] Perturbation injection released (`scripts/perturbation.py`)
- [x] Statistical testing released (`evaluation/statistical_tests.py`)
- [x] Annotation platform released (`annotation_platform/`)

## Training

- [x] All hyperparameters reported (`configs/training_config.yaml`)
- [x] Optimizer, learning rate, schedule documented
- [x] Batch size, epochs, early stopping criterion documented
- [x] Hardware requirements documented (1× NVIDIA A100 80GB)
- [x] Random seeds reported (42, 123, 2024)
- [x] LoRA configuration documented (r=16, α=32, dropout=0.05)

## Evaluation

- [x] Defect detection metrics (Precision, Recall, F1)
- [x] Additional metrics (Accuracy, Specificity, AUC)
- [x] Human alignment (Pearson r, Spearman ρ, Kendall τ)
- [x] Statistical tests (McNemar, bootstrap 95% CI)
- [x] Effect size (Cohen's d, Cliff's delta)
- [x] Cross-dataset protocol documented
- [x] Ablation study configs released

## Ethics and License

- [x] IRB approval documented
- [x] Human consent and compensation documented
- [x] License specified (CC BY-NC-SA 4.0)

## Citation

BibTeX entry provided in README.md.
