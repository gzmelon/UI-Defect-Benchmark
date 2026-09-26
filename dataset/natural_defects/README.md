# Natural Defect Subset

In response to Reviewer #4 and Reviewer #5, we additionally mined and
manually validated 400 naturally occurring UI defects from open-source
frontend repositories.

## Mining Protocol

- Source repositories: React, Vue, Bootstrap projects on GitHub
- Selection: issues labeled "bug", "ui", or "layout" with visual evidence
- Validation: 3 independent annotators confirmed each defect
- Inter-rater agreement: Cohen's κ = 0.81

## Defect Distribution

| Category | Count |
|---|---|
| CSS Occlusion | 124 |
| Spatial Misalignment | 98 |
| Contrast Violation | 82 |
| Text Overflow | 61 |
| Missing Asset | 35 |

## Usage

These natural defects are used exclusively for out-of-distribution
testing. They are **not** part of the training set. NS-CQA achieves
F1 = 0.862 on this subset, compared with F1 = 0.914 on the synthetic
benchmark (a gap of 5.2 points).
