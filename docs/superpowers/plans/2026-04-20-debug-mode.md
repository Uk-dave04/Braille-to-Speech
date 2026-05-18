# Debug Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a debug mode that saves intermediate Braille-processing artifacts for each upload and shows them on the result page.

**Architecture:** The pipeline will own debug-artifact generation so image-processing concerns stay out of Flask route code. The app will pass through debug metadata and serve saved debug files through a dedicated route.

**Tech Stack:** Python 3.11, Flask, OpenCV, pytest, dataclasses, pathlib

---

## Proposed File Structure

- Modify: `app.py`
- Modify: `src/braille_system/pipeline.py`
- Modify: `templates/result.html`
- Create: `tests/test_debug_mode.py`
- Modify: `tests/test_app.py`
- Modify: `README.md`

### Task 1: Add Pipeline Debug Artifact Support

**Files:**
- Modify: `src/braille_system/pipeline.py`
- Test: `tests/test_debug_mode.py`

- [ ] Write a failing test for timestamped debug-folder creation and artifact-path return
- [ ] Run `.\.venv\Scripts\python -m pytest tests/test_debug_mode.py -v` and confirm it fails
- [ ] Extend `RecognitionResult` with debug-path metadata and model-usage metadata
- [ ] Save original image, binary image, and detection-overlay image into `debug/<upload-stem>-<timestamp>/`
- [ ] Run `.\.venv\Scripts\python -m pytest tests/test_debug_mode.py -v` and confirm it passes

### Task 2: Add Flask Debug File Serving And Result Rendering

**Files:**
- Modify: `app.py`
- Modify: `templates/result.html`
- Modify: `tests/test_app.py`

- [ ] Write a failing test that expects debug artifacts to appear on the result page
- [ ] Run `.\.venv\Scripts\python -m pytest tests/test_app.py -v` and confirm it fails
- [ ] Add a Flask route for serving saved debug files
- [ ] Render debug metadata and debug images on `result.html`
- [ ] Run `.\.venv\Scripts\python -m pytest tests/test_app.py -v` and confirm it passes

### Task 3: Document And Verify Debug Mode

**Files:**
- Modify: `README.md`

- [ ] Add a README section explaining where debug artifacts are saved and how to inspect them
- [ ] Run `.\.venv\Scripts\python -m pytest -v`
- [ ] Confirm the full suite stays green after the debug-mode changes

## Self-Review Notes

- **Spec coverage:** The plan covers saved artifacts, result-page visibility, metadata, per-upload folder naming, and dedicated file serving.
- **Placeholder scan:** No `TODO`, `TBD`, or deferred placeholders remain in this plan.
- **Type consistency:** The plan consistently refers to `RecognitionResult`, debug artifact paths, and Flask debug-file serving without introducing mismatched helper names.
