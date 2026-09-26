# Natural Defect Subset

In response to Reviewer #4 and Reviewer #5, we mined and manually
validated 400 naturally occurring UI defects from open-source frontend
repositories.

## Source Repositories

- `facebook/react`
- `vuejs/core`
- `twbs/bootstrap`
- `angular/angular`
- `sveltejs/svelte`

## Mining Protocol

1. Fetch closed issues labeled `bug`, `ui`, `layout`, `css`, or `visual`.
2. Filter for issues that contain visual evidence (screenshots, CSS).
3. Manually classify the defect type.
4. Three independent annotators confirm each candidate.
5. Inter-rater agreement: Cohen's κ = 0.81.

## Distribution

| Category | Count |
|---|---|
| CSS Occlusion | 124 |
| Spatial Misalignment | 98 |
| Contrast Violation | 82 |
| Text Overflow | 61 |
| Missing Asset | 35 |
| **Total** | **400** |

## Usage

These natural defects are used exclusively for out-of-distribution
testing. They are **not** part of the training set.

## Performance

| Dataset | NS-CQA F1 |
|---|---|
| Synthetic Figma-Defect-3.5K | 0.914 |
| Natural open-source defects (400) | 0.862 |
| Gap | 5.2 points |

## Files

- `annotations_sample.json` — 10 sample entries
- `candidates.json` — full candidate list (requires GitHub mining)
- `mine_natural_defects.py` — mining script

## License

CC BY-NC-SA 4.0 for academic research purposes.
