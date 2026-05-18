# Page Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve full-page recognition by normalizing the page area and using spacing-aware grouping.

**Architecture:** `preprocess.py` will isolate and normalize the primary page region before thresholding. `segment.py` will infer grouping tolerances from detected dots rather than relying only on fixed gap values.

**Tech Stack:** Python, OpenCV, NumPy, pytest

---

### Task 1: Preprocess tests

**Files:**
- Modify: `tests/test_preprocess.py`

- [x] Add failing tests for page cropping and binary output preservation.
- [x] Run `pytest tests/test_preprocess.py -q` and verify failure.

### Task 2: Page normalization

**Files:**
- Modify: `src/braille_system/preprocess.py`

- [x] Implement page-region cropping and stronger normalization.
- [x] Run `pytest tests/test_preprocess.py -q` and verify pass.

### Task 3: Spacing-aware grouping

**Files:**
- Modify: `tests/test_segment.py`
- Modify: `src/braille_system/segment.py`

- [x] Add failing tests for spacing-aware grouping on uneven cell spacing.
- [x] Run `pytest tests/test_segment.py -q` and verify failure.
- [x] Implement dynamic spacing estimation from detected dot boxes.
- [x] Run `pytest tests/test_segment.py -q` and verify pass.

### Task 4: Full verification

**Files:**
- Modify: `docs/superpowers/plans/2026-05-11-page-normalization.md`

- [x] Run `pytest -q` and verify the full suite remains green.
- [x] Mark the plan complete after verification.
