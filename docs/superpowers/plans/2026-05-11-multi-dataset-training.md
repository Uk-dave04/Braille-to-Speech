# Multi-Dataset Training Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Support training and evaluation from multiple processed dataset roots.

**Architecture:** Dataset collection will accept a list of processed roots and concatenate samples while preserving the existing class-folder label convention. Train and evaluate will resolve dataset roots from one helper so the workflow stays consistent.

**Tech Stack:** Python, TensorFlow, OpenCV, pytest

---

### Task 1: Dataset collection

**Files:**
- Modify: `src/braille_system/modeling/dataset.py`
- Modify: `tests/test_dataset.py`

- [x] Add failing tests for collecting samples from multiple roots.
- [x] Run `pytest tests/test_dataset.py -q` and verify failure.
- [x] Implement multi-root collection helpers.
- [x] Run `pytest tests/test_dataset.py -q` and verify pass.

### Task 2: Train/evaluate integration

**Files:**
- Modify: `src/braille_system/modeling/train.py`
- Modify: `src/braille_system/modeling/evaluate.py`

- [x] Update loading to accept one or more dataset roots.
- [x] Resolve dataset roots from one helper.
- [x] Verify train/evaluate imports still work with tests.

### Task 3: Docs

**Files:**
- Modify: `README.md`
- Create: `src/braille_system/modeling/prepare_dsbi_dataset.py`
- Test: `tests/test_prepare_dsbi_dataset.py`
- Modify: `docs/superpowers/plans/2026-05-11-multi-dataset-training.md`

- [x] Document recommended additional datasets and the multi-dataset workflow.
- [x] Add a DSBI-specific processor that converts page annotations into folder-per-class crops.
- [x] Verify the DSBI processor with focused tests.
- [x] Run `pytest -q` and verify the full suite remains green.
- [x] Mark the plan complete after verification.
