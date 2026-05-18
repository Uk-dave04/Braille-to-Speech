# Braille-to-Speech MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a research prototype that accepts an uploaded Braille image, preprocesses and segments Braille cells, classifies each cell with a CNN, reconstructs Grade 1 English text, and generates Yoruba-capable speech output in a local Flask app.

**Architecture:** The app is split into focused modules for preprocessing, segmentation, CNN training, inference, decoding, reconstruction, speech, and web presentation. The model predicts 6-dot Braille patterns, while a separate decoder maps those patterns into text.

**Tech Stack:** Python 3.11, Flask, OpenCV, NumPy, TensorFlow/Keras, scikit-learn, pytest, gTTS

---

## Proposed File Structure

- `README.md`
- `requirements.txt`
- `.gitignore`
- `app.py`
- `config.py`
- `src/braille_system/preprocess.py`
- `src/braille_system/segment.py`
- `src/braille_system/decode.py`
- `src/braille_system/reconstruct.py`
- `src/braille_system/inference.py`
- `src/braille_system/tts.py`
- `src/braille_system/modeling/dataset.py`
- `src/braille_system/modeling/model.py`
- `src/braille_system/modeling/train.py`
- `src/braille_system/modeling/evaluate.py`
- `templates/index.html`
- `templates/result.html`
- `static/style.css`
- `tests/test_decode.py`
- `tests/test_preprocess.py`
- `tests/test_reconstruct.py`
- `tests/test_model.py`
- `tests/test_dataset.py`
- `tests/test_tts.py`
- `tests/test_app.py`

### Task 1: Bootstrap the Project

**Files:**
- Create: `README.md`
- Create: `requirements.txt`
- Create: `.gitignore`

- [ ] Initialize git with `git init`
- [ ] Create `requirements.txt` with Flask, OpenCV, NumPy, TensorFlow, scikit-learn, matplotlib, seaborn, gTTS, Pillow, pytest, pytest-cov
- [ ] Create `.gitignore` for virtualenvs, caches, generated uploads, audio files, and model files
- [ ] Create `README.md` with setup commands and a one-paragraph project description
- [ ] Create `.venv` and install dependencies with `pip install -r requirements.txt`
- [ ] Commit with `git commit -m "chore: bootstrap braille project"`

### Task 2: Set Up Configuration and Project Layout

**Files:**
- Create: `config.py`
- Create: `src/braille_system/__init__.py`
- Create: `src/braille_system/io.py`
- Create: `tests/conftest.py`

- [ ] Write a failing test that confirms runtime directories are created
- [ ] Implement `ensure_runtime_dirs()` for `uploads/` and `outputs/audio/`
- [ ] Add `config.py` constants for `UPLOAD_DIR`, `AUDIO_DIR`, and `MODEL_PATH`
- [ ] Add `tests/conftest.py` so `src/` imports resolve during pytest
- [ ] Run `pytest tests/conftest.py -v`
- [ ] Commit with `git commit -m "feat: add configuration helpers"`

### Task 3: Implement Braille Mapping and Decoder

**Files:**
- Create: `src/braille_system/decode.py`
- Create: `tests/test_decode.py`

- [ ] Write failing tests for simple letters, spaces, and number-mode decoding
- [ ] Implement Grade 1 mapping as 6-bit string patterns
- [ ] Support number sign handling and unknown-pattern fallback
- [ ] Run `pytest tests/test_decode.py -v`
- [ ] Commit with `git commit -m "feat: add grade 1 braille decoder"`

### Task 4: Build the Preprocessing Pipeline

**Files:**
- Create: `src/braille_system/preprocess.py`
- Create: `tests/test_preprocess.py`

- [ ] Write a failing smoke test that checks output shape and binary image values
- [ ] Implement grayscale conversion, Gaussian blur, histogram equalization, adaptive thresholding, and morphology cleanup
- [ ] Add helper functions for deskew and normalization if needed after first tests
- [ ] Run `pytest tests/test_preprocess.py -v`
- [ ] Commit with `git commit -m "feat: add image preprocessing pipeline"`

### Task 5: Build Segmentation and Spatial Ordering

**Files:**
- Create: `src/braille_system/segment.py`
- Create: `src/braille_system/reconstruct.py`
- Create: `tests/test_reconstruct.py`

- [ ] Write a failing test for grouping cells into lines based on y-position tolerance
- [ ] Implement contour-based candidate extraction in `segment.py`
- [ ] Implement `sort_cells_into_lines()` in `reconstruct.py`
- [ ] Add a second failing test for joining decoded line outputs with line breaks
- [ ] Implement `reconstruct_text_lines()`
- [ ] Run `pytest tests/test_reconstruct.py -v`
- [ ] Commit with `git commit -m "feat: add cell grouping and reconstruction"`

### Task 6: Define the CNN Architecture

**Files:**
- Create: `src/braille_system/modeling/model.py`
- Create: `src/braille_system/modeling/__init__.py`
- Create: `tests/test_model.py`

- [ ] Write a failing test that checks model output shape is `(None, 64)` for 64 classes
- [ ] Implement a compact CNN with 3 convolution blocks, max pooling, dropout, and a softmax output layer
- [ ] Compile with Adam and categorical cross-entropy
- [ ] Run `pytest tests/test_model.py -v`
- [ ] Commit with `git commit -m "feat: add braille cnn model"`

### Task 7: Add Dataset Loading and Training

**Files:**
- Create: `data/README.md`
- Create: `src/braille_system/modeling/dataset.py`
- Create: `src/braille_system/modeling/train.py`
- Create: `tests/test_dataset.py`

- [ ] Document dataset folder format as `data/processed/<pattern_label>/<image>.png`
- [ ] Write a failing test for collecting labeled image paths from class folders
- [ ] Implement `collect_image_paths()` and dataset loading
- [ ] Implement train/validation split with `train_test_split(..., stratify=...)`
- [ ] Add model checkpointing to `models/braille_cnn.keras`
- [ ] Run `pytest tests/test_dataset.py -v`
- [ ] Run `python -m src.braille_system.modeling.train`
- [ ] Commit with `git commit -m "feat: add training pipeline"`

### Task 8: Add Evaluation and Accuracy Diagnostics

**Files:**
- Create: `src/braille_system/modeling/evaluate.py`
- Modify: `README.md`

- [ ] Implement classification report and confusion matrix generation
- [ ] Save the confusion matrix image to `outputs/confusion_matrix.png`
- [ ] Add a README section called `Accuracy improvement checklist`
- [ ] Include actions for augmentation, balancing classes, reviewing confusion pairs, and tuning thresholding
- [ ] Run `python -m src.braille_system.modeling.evaluate`
- [ ] Commit with `git commit -m "feat: add model evaluation tooling"`

### Task 9: Add Inference Utilities

**Files:**
- Create: `src/braille_system/inference.py`
- Modify: `src/braille_system/reconstruct.py`

- [ ] Implement `load_inference_model()`
- [ ] Implement `prepare_cell_for_model()` to resize to `32x32`, normalize, and add batch/channel dimensions
- [ ] Implement `predict_braille_pattern()` to return `(pattern, confidence)`
- [ ] Reuse the reconstruction helpers to produce multiline decoded text
- [ ] Add tests for confidence range and output types if fixtures are available
- [ ] Run `pytest tests/test_reconstruct.py -v`
- [ ] Commit with `git commit -m "feat: add inference helpers"`

### Task 10: Add Yoruba-Capable TTS

**Files:**
- Create: `src/braille_system/tts.py`
- Create: `tests/test_tts.py`

- [ ] Write a failing test for audio output filename generation
- [ ] Implement `build_audio_output_path()` for `.mp3` output
- [ ] Implement `synthesize_text_to_speech(text, output_path, lang="yo")`
- [ ] Add a fallback path or clear exception for TTS service failures
- [ ] Run `pytest tests/test_tts.py -v`
- [ ] Commit with `git commit -m "feat: add yoruba tts service"`

### Task 11: Build the Flask Interface

**Files:**
- Create: `app.py`
- Create: `templates/index.html`
- Create: `templates/result.html`
- Create: `static/style.css`
- Create: `tests/test_app.py`

- [ ] Write failing tests for `GET /` and missing-file validation on `POST /predict`
- [ ] Implement the upload form on `/`
- [ ] Implement `/predict` with validation and result rendering
- [ ] Add a simple result page showing recognized text and an audio player
- [ ] Run `pytest tests/test_app.py -v`
- [ ] Commit with `git commit -m "feat: add flask upload interface"`

### Task 12: Connect the End-to-End Pipeline

**Files:**
- Modify: `app.py`
- Modify: `src/braille_system/preprocess.py`
- Modify: `src/braille_system/segment.py`
- Modify: `src/braille_system/inference.py`

- [ ] Save the uploaded image to `uploads/`
- [ ] Read the image with OpenCV
- [ ] Preprocess and segment candidate cells
- [ ] Classify each cell and attach confidence values
- [ ] Group cells into lines and reconstruct the decoded text
- [ ] Generate speech output into `outputs/audio/`
- [ ] Return the result page with text and audio
- [ ] Run `pytest -v`
- [ ] Launch `python app.py` and verify manual upload flow
- [ ] Commit with `git commit -m "feat: connect full braille pipeline"`

### Task 13: Prepare Demo Assets and Final Validation

**Files:**
- Modify: `README.md`
- Create: `tests/fixtures/sample_images/`
- Create: `tests/fixtures/sample_cells/`

- [ ] Add a `Demo workflow` section to `README.md`
- [ ] Add a `Current limitations` section to `README.md`
- [ ] Collect a few clean sample Braille images for tests and presentation
- [ ] Run `python -m src.braille_system.modeling.train`
- [ ] Run `python -m src.braille_system.modeling.evaluate`
- [ ] Run `pytest -v`
- [ ] Run `python app.py`
- [ ] Record model path, audio output path, and confusion-matrix output path in the README
- [ ] Commit with `git commit -m "docs: prepare braille mvp demo guide"`

## Self-Review Notes

- **Spec coverage:** The plan covers upload input, preprocessing, segmentation, CNN training, inference, Grade 1 Braille decoding, sentence reconstruction, Flask presentation, and Yoruba-capable TTS.
- **Placeholder scan:** No `TODO`, `TBD`, or deferred-placeholder text remains in the plan itself.
- **Type consistency:** The planned helper names are consistent across tasks: `preprocess_braille_image`, `sort_cells_into_lines`, `reconstruct_text_lines`, `decode_braille_patterns`, `build_braille_cnn`, and `predict_braille_pattern`.
