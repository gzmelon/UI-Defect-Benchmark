# Annotation Guidelines for Figma-Defect-3.5K

## Purpose

This document describes the protocol used by 50 human UX experts to
score UI component quality on a 1-100 MOS scale.

## Procedure

For each UI component, the annotator is shown:

1. The rendered screenshot at 1920×1080.
2. The corresponding DOM snippet (tag, classes, inline styles).
3. The computed style metadata for the responsible node.

The annotator then answers:

- **Q1**: What is the primary defect? (choose 1 of 5 categories)
- **Q2**: How severe is it? (`critical` / `major` / `minor`)
- **Q3**: What is the overall quality? (1-100 MOS)
- **Q4**: What is the suggested repair? (free text, optional)

## Defect Categories

| Category | Definition |
|---|---|
| CSS Occlusion | One element visually blocks another |
| Spatial Misalignment | Flexbox/Grid layout does not align as expected |
| Contrast Violation | Foreground/background contrast < WCAG AA |
| Text Overflow | Text extends beyond its container |
| Missing Asset | Image or icon fails to render |

## Severity Rubric

- **Critical**: Blocks user task or severely degrades usability
- **Major**: Noticeable to most users; requires attention
- **Minor**: Cosmetic; little impact on task completion

## Quality Control

- Each component scored by 3 independent experts.
- Fleiss' Kappa computed across all 3 raters (threshold: κ ≥ 0.70).
- Disagreements > 20 MOS points trigger a 4th expert arbitration.
- Annotators compensated at $25/hour (industry standard).

## Example

**Component**: A "Submit" button occluded by a fixed "Cookie Banner".

- Q1: CSS Occlusion
- Q2: Critical (blocks primary action)
- Q3: 32 / 100 (very low quality)
- Q4: "Reduce z-index of banner or add bottom margin."

## Training

All annotators completed a 2-hour calibration session on 20 sample
components before beginning the main annotation task.

## Ethics

IRB approval was obtained from Guangzhou University of Software.
All annotators provided informed consent.
