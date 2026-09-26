# Cross-Dataset Evaluation Protocol: WebArena Offline Snapshots

## Clarification

Our cross-dataset test uses **offline rendered snapshots** of WebArena pages,
not interactive agent tasks.

## Protocol

1. Sampled 2,000 interactive elements from WebArena pages.
2. Each page loaded in headless Chromium (Playwright).
3. Captured static DOM at the decision point.
4. Serialized DOM as JSON; extracted computed styles.
5. Evaluated model on (static DOM, screenshot, bounding box).
6. Dynamic interactive tasks are evaluated separately in Section 5.7.

## Results

| Dataset | NS-CQA F1 | LLaVA-1.5 F1 | p-value |
|---|---|---|---|
| Figma-Defect-3.5K | 0.914 | 0.858 | < 0.01 |
| WebArena subset (2,000) | 0.862 | 0.812 | < 0.01 |
