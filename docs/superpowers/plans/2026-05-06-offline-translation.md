# Offline Translation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the online translation dependency with a deterministic offline English-to-Yoruba translator.

**Architecture:** The translation layer remains isolated in `translation.py`, but instead of calling an external service it uses a local phrase dictionary, token dictionary, and light text cleanup. The Flask app continues to consume a `TranslationResult` and chooses Yoruba or English speech based on whether any offline translation occurred.

**Tech Stack:** Python, Flask, pytest, eSpeak

---

### Task 1: Offline translator behavior

**Files:**
- Modify: `src/braille_system/translation.py`
- Test: `tests/test_translation.py`

- [x] Write failing tests for exact phrase translation, token translation, and unknown-word fallback.
- [x] Run `pytest tests/test_translation.py -q` and verify failure against the old online implementation.
- [x] Implement the local phrase-plus-dictionary translator.
- [x] Run `pytest tests/test_translation.py -q` and verify pass.

### Task 2: App integration

**Files:**
- Modify: `app.py`
- Modify: `tests/test_app.py`

- [x] Update tests so Yoruba audio is used when at least one offline translation occurs and English audio is used when none occurs.
- [x] Run `pytest tests/test_app.py -q` and verify failure if assumptions still match the online translator.
- [x] Keep the Flask route contract stable while removing online dependency assumptions.
- [x] Run `pytest tests/test_app.py -q` and verify pass.

### Task 3: Dependency and docs cleanup

**Files:**
- Modify: `requirements.txt`
- Modify: `README.md`

- [x] Remove the online translation dependency.
- [x] Update the README to describe the offline translator limits clearly.
- [x] Run the full suite with `pytest -q` and verify the integrated system remains green.
