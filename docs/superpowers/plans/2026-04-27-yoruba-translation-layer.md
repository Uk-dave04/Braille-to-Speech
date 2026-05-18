# Yoruba Translation Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an online English-to-Yoruba translation step between Braille recognition and speech generation.

**Architecture:** Keep recognition unchanged, add a focused translation module, then route translated Yoruba text into TTS while preserving graceful fallback to English audio if translation is unavailable.

**Tech Stack:** Python, Flask, deep-translator, gTTS, pytest

---

### Task 1: Translation service

**Files:**
- Create: `src/braille_system/translation.py`
- Test: `tests/test_translation.py`

- [x] Write failing tests for translation success and fallback.
- [x] Implement a small translation result object and online translator wrapper.
- [x] Verify the translation tests pass.

### Task 2: App integration

**Files:**
- Modify: `app.py`
- Modify: `templates/result.html`
- Test: `tests/test_app.py`

- [x] Write or extend failing tests for translated Yoruba output and English fallback audio.
- [x] Route recognized English text through the translation layer before TTS.
- [x] Render English text, Yoruba text, and fallback state in the result page.
- [x] Verify the app tests pass.

### Task 3: Runtime and docs

**Files:**
- Modify: `requirements.txt`
- Modify: `README.md`

- [x] Add the online translation dependency.
- [x] Update project docs so the runtime behavior matches the implementation.
- [x] Run the full test suite and confirm the integrated system remains green.
