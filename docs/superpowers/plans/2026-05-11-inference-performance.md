# Inference Performance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce inference latency by caching the model, disabling debug saves by default, and batching predictions.

**Architecture:** The pipeline keeps the same external API but moves model reuse into a module-level cache, adds an opt-in debug save flag, and replaces repeated per-cell prediction calls with one batched model inference step.

**Tech Stack:** Python, Flask, TensorFlow, pytest

---

### Task 1: Batch inference

**Files:**
- Modify: `src/braille_system/inference.py`
- Modify: `tests/test_inference_predict.py`

- [x] Add failing tests for batched prediction output.
- [x] Run `pytest tests/test_inference_predict.py -q` and verify failure.
- [x] Implement batch preparation and batched prediction helpers.
- [x] Run `pytest tests/test_inference_predict.py -q` and verify pass.

### Task 2: Pipeline caching and debug toggle

**Files:**
- Modify: `src/braille_system/pipeline.py`
- Modify: `tests/test_pipeline.py`

- [x] Add failing tests for model caching and disabled debug saving by default.
- [x] Run `pytest tests/test_pipeline.py -q` and verify failure.
- [x] Implement model caching, debug-save toggle, and pipeline use of batched predictions.
- [x] Run `pytest tests/test_pipeline.py -q` and verify pass.

### Task 3: Verification

**Files:**
- Modify: `docs/superpowers/plans/2026-05-11-inference-performance.md`

- [x] Run `pytest -q` and verify the full suite remains green.
- [x] Mark the plan complete after verification.
