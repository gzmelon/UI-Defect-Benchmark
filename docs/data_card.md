# Data Card: Figma-Defect-3.5K

## Overview

Figma-Defect-3.5K is a benchmark dataset for cross-modal UI defect
detection, consisting of 3,500 annotated UI components with
human-validated perturbations.

## Motivation

AI-generated frontends frequently contain latent defects spanning both
symbolic code (missing ARIA, invalid CSS) and visual rendering (z-index
occlusion, flexbox misalignment). Existing benchmarks are either
code-only or image-only, so they cannot evaluate methods that must
reason across modalities.

## Composition

| Attribute | Value |
|---|---|
| Total samples | 3,500 |
| Defect categories | 5 |
| Annotators | 50 (3 per sample) |
| Total evaluations | 10,500 |
| Inter-rater agreement | κ = 0.78 (Fleiss) |
| Injection methods | inline (50%), external (50%) |
| Mean MOS score | 52.4 (σ = 14.1) |

## Splits

| Split | Size | Purpose |
|---|---|---|
| Train | 2,450 (70%) | Model training |
| Val | 525 (15%) | Hyperparameter tuning |
| Test | 525 (15%) | Final evaluation |

## Natural Defect Subset

400 naturally occurring defects mined from open-source repositories
(React, Vue, Bootstrap). Used exclusively for out-of-distribution testing.

## Collection Process

1. Sourced 3,500 high-fidelity UI designs from the Figma community.
2. Applied automated AST perturbations to the corresponding HTML/CSS.
3. Rendered screenshots using headless Chromium at 1920×1080.
4. Extracted DOM trees and computed styles.
5. Asked 3 independent experts per component for MOS scores.

## Known Limitations

- Defects are programmatically synthesized, which may carry distribution
  bias relative to naturally occurring bugs.
- Dynamic UI states (:hover, :focus, JS modals) are not represented.
- Mobile and cross-browser rendering differences are partially covered.

## License

CC BY-NC-SA 4.0 for academic research purposes.

## Maintenance

Contact the corresponding author via the journal system.
