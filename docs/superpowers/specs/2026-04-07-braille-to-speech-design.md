# Braille-to-Speech Assistive System MVP Design

**Date:** 2026-04-07

## Goal

Build a research prototype that accepts a clear uploaded image of Grade 1 English Braille, preprocesses it, segments Braille cells, classifies each cell with a CNN, reconstructs readable text, and reads the result aloud through a Yoruba-capable TTS layer.

## Scope

### In scope

- Upload a Braille image through a web page
- Preprocess image with OpenCV
- Segment Braille cells
- Classify each 6-dot cell as a 6-bit pattern
- Decode Grade 1 English Braille text
- Generate speech audio with a Yoruba-capable TTS backend
- Show text, confidence summary, and audio playback

### Out of scope

- Live video
- Grade 2 contracted Braille
- Native Yoruba Braille recognition rules
- Mobile deployment

## Architecture

Pipeline:

`image upload -> preprocessing -> cell segmentation -> CNN classification -> sequence reconstruction -> Braille decoding -> text normalization -> TTS -> result page`

Modules:

- `input`: Flask upload handling
- `preprocess`: grayscale, denoise, threshold, normalize, deskew
- `segment`: locate and crop ordered Braille cells
- `model`: CNN that predicts 6-dot patterns
- `reconstruct`: group cells into lines and sequence them
- `decode`: convert Braille patterns into Grade 1 English text
- `tts`: generate Yoruba-capable speech audio
- `ui`: show uploaded image, recognized text, and audio player

## Technical Stack

- Python 3.11
- OpenCV, NumPy
- TensorFlow / Keras
- Flask
- scikit-learn
- Matplotlib / Seaborn
- gTTS first, with a pluggable speech interface for later engine replacement

## Hardware

- Laptop: Core i5 or Ryzen 5, 8 GB RAM minimum, 16 GB preferred
- Camera: 1080p webcam or smartphone camera
- Lighting: diffused white light, plain matte background, stable capture distance

## Data Representation

Represent each Braille cell as a 6-bit pattern in this order:

- dot 1: upper-left
- dot 2: middle-left
- dot 3: lower-left
- dot 4: upper-right
- dot 5: middle-right
- dot 6: lower-right

Examples:

- `100000` -> only dot 1 raised
- `110000` -> dots 1 and 2 raised
- `001111` -> number sign

The CNN predicts patterns, not letters. The decoder handles text rules.

## Braille Mapping Strategy

The MVP targets Grade 1 English Braille:

- letters `a-z`
- common punctuation
- number sign plus digit decoding
- spaces and line breaks from reconstruction logic

Yoruba support in this MVP is at the TTS layer, not the Braille-recognition label space.

## Evaluation

Measure:

- cell-level accuracy, precision, recall, F1
- confusion matrix
- character and word reconstruction quality
- speech-output usefulness in a demo setting

## Testing

- unit tests for decoder and reconstruction
- preprocessing smoke tests
- training and evaluation scripts
- Flask route tests
- one end-to-end sample-image pipeline test

## Approved Design Summary

- MVP type: uploaded-image research prototype
- Recognition target: Grade 1 English Braille
- Model output: 6-dot patterns
- Interface: Flask web app
- Speech: Yoruba-capable TTS backend
- Priority: reliability, modularity, and demo readiness
