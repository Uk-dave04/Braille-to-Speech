# Page Normalization Design

## Goal

Improve recognition on full-page Braille photos by normalizing the page region before segmentation and by making cell grouping more spacing-aware.

## Approved Changes

- Add a page cropping step that keeps the main bright page region and removes more background.
- Strengthen preprocessing for uneven lighting and page-level noise.
- Improve cell grouping with spacing-aware thresholds derived from detected dot geometry instead of fixed constants alone.

## Scope

- Keep the public Flask workflow unchanged.
- Keep the CNN, offline translation, and offline TTS unchanged.
- Extend preprocessing and segmentation only.

## Expected Outcome

- More stable page area for segmentation.
- Better horizontal and vertical dot grouping across full-page images.
- Fewer missed characters caused by inconsistent spacing.

## Limits

- This still will not fully solve severe perspective distortion or poor camera focus.
- Retraining may still be needed after the page-level inputs improve.
