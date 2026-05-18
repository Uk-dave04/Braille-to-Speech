# Debug Mode Design For Braille Upload Diagnostics

**Date:** 2026-04-19

## Goal

Add a debug mode to the Braille-to-Speech prototype so each upload produces inspectable intermediate artifacts that explain why segmentation succeeds or fails.

## Scope

### In scope

- Save debug artifacts for each upload
- Show debug artifacts on the result page
- Expose original image, binary/preprocessed image, and detection overlay
- Surface metadata such as detected cell count, average confidence, and whether a trained model was used
- Keep the normal recognition flow working even when no cells are found

### Out of scope

- Full image-analysis dashboard
- User authentication or multi-user history
- Persistent database storage

## Debug Artifacts

For each upload, the app will produce:

- original uploaded image
- preprocessed binary image
- bounding-box overlay image showing detected candidate cells
- metadata summary for the run

## Storage Strategy

Each upload will create a timestamped debug folder:

`debug/<upload-stem>-<timestamp>/`

This avoids collisions and keeps runs easy to compare.

## Runtime Behavior

- Debug mode is enabled by default for the current development phase
- The pipeline will save debug images during processing
- The Flask app will render those artifacts on the result page
- A dedicated route will serve saved debug files

## Failure Interpretation

- If the binary image is poor, preprocessing needs improvement
- If the binary image is good but there are no boxes, segmentation needs improvement
- If boxes exist but text is poor, model inference or decoding needs improvement

## Implementation Notes

- Extend the pipeline result object with debug metadata and file paths
- Save debug images from the pipeline so app logic stays thin
- Render debug images and metadata in `result.html`
- Add tests for debug-folder creation, path propagation, and result-page rendering

## Approved Design Summary

- Save debug artifacts to disk
- Show them in the result page
- Use timestamped per-upload folders
- Keep debug mode on by default while diagnosing segmentation
