# Multi-Dataset Training Design

## Goal

Allow the training and evaluation pipeline to combine multiple processed Braille datasets so the model can learn from more realistic image distributions.

## Recommended Datasets

- `braille_segment_character_natural` for cropped labeled character images already in the project.
- `DSBI` for denser full-page embossed Braille images and annotations.
- `AngelinaDataset` for realistic camera-style Braille page photos.

## Approved Changes

- Extend dataset collection so it can read one or more processed dataset roots.
- Keep the class-label scheme unchanged: each class remains a 6-bit pattern folder.
- Allow train/evaluate commands to consume multiple dataset directories through one configuration entry point.

## Scope

- No model architecture change in this pass.
- No change to existing processed dataset layout.
- Only dataset loading, training entrypoints, and docs change.

## Expected Outcome

- Easier retraining on mixed data sources.
- Better domain coverage for full-page camera photos once additional datasets are processed into the same folder-per-class format.
