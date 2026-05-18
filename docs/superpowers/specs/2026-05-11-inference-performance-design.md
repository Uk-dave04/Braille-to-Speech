# Inference Performance Design

## Goal

Reduce request latency in the Braille recognition pipeline without changing the user-facing workflow.

## Approved Changes

- Cache the loaded TensorFlow model in memory instead of loading it on every request.
- Make debug artifact saving optional and disabled by default for normal runs.
- Batch cell predictions so the model processes all detected cells in one call rather than one `predict` call per cell.

## Scope

- No change to Flask routes or result-page content.
- No change to the Braille decoding rules.
- No segmentation rewrite in this pass.

## Expected Impact

- Lower startup cost per request from model reuse.
- Less disk I/O from skipping debug image writes during normal processing.
- Faster inference on multi-cell images by reducing repeated TensorFlow calls.

## Limits

- This will improve speed, but it will not fully solve bad recognition on full-page images.
- Segmentation quality remains the main cause of missed characters.
