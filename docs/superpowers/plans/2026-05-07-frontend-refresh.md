# Frontend Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the frontend into a polished product-style UI and remove debug images from the result page.

**Architecture:** Keep the Flask routes unchanged and implement the refresh through template structure plus a shared stylesheet. The result page remains text-and-audio focused, while debug artifacts stay in backend data only and are no longer rendered to users.

**Tech Stack:** Flask templates, CSS, pytest

---

### Task 1: Result-page contract

**Files:**
- Modify: `tests/test_app.py`
- Modify: `templates/result.html`

- [x] Write failing tests that remove the debug gallery expectation and assert the result page remains text/audio focused.
- [x] Run `pytest tests/test_app.py -q` and verify failure.
- [x] Update the result template to remove debug images and keep only product-facing content.
- [x] Run `pytest tests/test_app.py -q` and verify pass.

### Task 2: Product-style layout

**Files:**
- Modify: `templates/index.html`
- Modify: `templates/result.html`
- Modify: `static/style.css`

- [x] Add semantic layout wrappers and class names for a product-style upload and results experience.
- [x] Implement responsive CSS for hero, cards, actions, metadata, and audio sections.
- [x] Verify the templates still render with the Flask app.

### Task 3: Full verification

**Files:**
- Modify: `docs/superpowers/plans/2026-05-07-frontend-refresh.md`
- Modify: `README.md` if UI wording needs alignment

- [x] Run `pytest -q` and verify the full suite remains green.
- [x] Mark the plan complete after verification.
