# Dot-First Segmentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace contour-only cell extraction with dot-first grouping for full-page Braille photos.

**Architecture:** `segment.py` will detect small dot contours, cluster them into lines, then merge dot groups into inferred cell boxes. The pipeline interface remains unchanged and continues to feed grouped crops into the CNN and reconstruction stages.

**Tech Stack:** Python, OpenCV, NumPy, pytest

---

### Task 1: Segmentation tests

**Files:**
- Modify: `tests/test_segment.py`

- [x] Add failing tests for dot detection and grouped cell extraction.
- [x] Run `pytest tests/test_segment.py -q` and verify failure.

### Task 2: Dot-first grouping

**Files:**
- Modify: `src/braille_system/segment.py`

- [x] Implement dot contour detection and line-aware cell grouping.
- [x] Run `pytest tests/test_segment.py -q` and verify pass.

### Task 3: Full verification

**Files:**
- Modify: `docs/superpowers/plans/2026-05-11-dot-first-segmentation.md`

- [x] Run `pytest -q` and verify the full suite remains green.
- [x] Mark the plan complete after verification.
