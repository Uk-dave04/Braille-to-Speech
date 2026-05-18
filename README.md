# Braille-to-Speech Assistive System

Research prototype for Braille-to-speech assistance using Gemini Vision for image-to-text recognition, Gemini for English-to-Yoruba translation, and Spitch for Yoruba speech output.

## Main pipeline

1. Upload image
2. Send image to Gemini Vision for Braille-to-English recognition
3. Translate English text to Yoruba with Gemini
4. Generate Yoruba speech with Spitch

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Demo workflow

1. Start the Flask app with `python app.py`
2. Open `http://127.0.0.1:5000`
3. Upload a clear Braille image
4. Review recognized English text
5. Review translated Yoruba text
6. Play generated speech audio

## Gemini setup

The live app now uses Gemini for both image-to-text recognition and English-to-Yoruba translation. Set your API key once and new terminals will inherit it after you reopen them:

```powershell
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-api-key", "User")
```

You can confirm it in a new PowerShell window with:

```powershell
echo $env:GEMINI_API_KEY
```

If Gemini is unavailable, the app returns an error for that request instead of silently falling back to another recognizer or translator.

## Spitch speech setup

The live app now uses Spitch for Yoruba TTS. Set your Spitch API key before starting the app:

```powershell
[System.Environment]::SetEnvironmentVariable("SPITCH_API_KEY", "your-spitch-api-key", "User")
```

Then close and reopen PowerShell before launching the Flask app.

## Render deployment note

The deployed app uses a longer Gunicorn timeout because Gemini recognition and Yoruba translation can take longer than the default 30 seconds on cold or busy requests.

If Spitch is unavailable, the app returns an error for that request instead of silently falling back to another speech engine.

## Training workflow

Prepare the cropped cell dataset:

```bash
python -m src.braille_system.modeling.prepare_character_dataset
```

Train the Braille CNN:

```bash
python -m src.braille_system.modeling.train
```

Evaluate the trained model:

```bash
python -m src.braille_system.modeling.evaluate
```

The prepared dataset currently lives in:

`data/processed/braille_segment_character_natural_ids`

To train from multiple processed datasets at once, set `BRAILLE_DATASET_DIRS` as a path-separated list before running training or evaluation.

PowerShell example:

```powershell
$env:BRAILLE_DATASET_DIRS = "C:\Users\User\Desktop\braille_dev\data\processed\braille_segment_character_natural_ids;C:\Users\User\Desktop\braille_dev\data\processed\angelina_ids"
python -m src.braille_system.modeling.train
python -m src.braille_system.modeling.evaluate
```

## Recommended additional datasets

For the current full-page camera-photo problem, the most useful additions are datasets that look more like real embossed Braille pages than clean single-cell crops.

- `DSBI (Double-Sided Braille Image Dataset)`
  - Strong for dense Braille page structure and realistic embossed layouts
  - Repository: [DSBI](https://github.com/yeluo1994/DSBI)

- `Angelina Braille Images Dataset`
  - Strong for real camera-style Braille page photos
  - Repository: [AngelinaDataset](https://github.com/IlyaOvodov/AngelinaDataset)

- `braille_segment_character_natural`
  - Keep this as your baseline cropped-cell dataset
  - Good for initial class coverage, but not enough alone for page-photo robustness

## Accuracy improvement checklist

- Add rotation, brightness, blur, and noise augmentation
- Balance underrepresented Braille-pattern classes
- Review common confusion pairs from the confusion matrix
- Tune thresholding and morphology parameters for segmentation quality
- Increase training samples across different lighting conditions

## Current behavior

- The app sends uploaded Braille images to Gemini Vision for English text recognition
- It then translates the English text to Yoruba with Gemini
- Yoruba speech is generated with Spitch from the translated Yoruba text
- If Gemini cannot be reached or returns empty text, the request returns an error
- If Spitch cannot synthesize audio, the request returns an error

## Current limitations

- Yoruba support is currently through English-to-Yoruba translation plus TTS, not native Yoruba Braille decoding
- Best results still depend on clear, well-lit uploaded images
- Live video recognition is not part of this MVP
- Recognition and translation depend on internet access and a valid Gemini API key
- Yoruba speech depends on internet access and a valid Spitch API key

## Current implemented modules

- Gemini Vision Braille-to-English recognition
- Gemini English-to-Yoruba translation
- Spitch Yoruba text-to-speech synthesis
- Character-dataset preparation from the `braille_segment_character_natural` archive
- Dataset folder scanning for Braille cell images
- Flask upload flow with file-type validation
- Model training, evaluation, and inference with TensorFlow
- Local CNN-based research pipeline retained in the codebase for training and experimentation
