# Dot-First Segmentation Design

## Goal

Improve full-page Braille recognition by replacing contour-as-cell segmentation with a dot-first grouping pipeline.

## Approved Flow

`preprocess page -> detect Braille dots -> cluster dots into lines -> infer Braille cells from dot geometry -> crop inferred cells -> classify with CNN -> reconstruct text`

## Scope

- Keep the CNN model, offline translation, and offline speech layers unchanged.
- Replace the logic in `segment.py` so candidate cells are inferred from detected dots rather than raw external contours.
- Keep the public pipeline entrypoint stable.

## Segmentation Strategy

- Detect small dot candidates from the binary page image.
- Filter dot candidates by contour size.
- Sort dots by line using Y-position clustering.
- Within each line, merge nearby dots into candidate cell boxes using horizontal gap tolerance.
- Expand cell boxes slightly so the CNN crop includes the full inferred cell region.

## Expected Outcome

- Fewer false cell boxes on dense page images.
- More stable ordering of cells within lines.
- Better reconstruction because grouped boxes align with Braille geometry instead of arbitrary blobs.

## Limits

- This is still a heuristic approach and will not fully solve perspective distortion or severe lighting issues.
- It should improve full-page handling enough to judge whether later retraining is necessary.
