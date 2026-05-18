# Gemini-Only Recognition Design

## Goal

Make Gemini Vision the only image-to-text recognizer in the live web app and return an error if Gemini cannot provide usable text.

## Architecture

- Upload image through Flask
- Send uploaded image to Gemini Vision
- Receive English text from Gemini
- Translate English text to Yoruba with the existing offline translator
- Generate speech with the existing eSpeak integration

## Error handling

- If `GEMINI_API_KEY` is missing, return an error
- If Gemini transport fails, return an error
- If Gemini returns empty text, return an error
- Do not silently fall back to the local OpenCV/CNN recognizer in the live app

## UI behavior

- Keep the same upload and result flow
- Remove local-model metrics from the result page because they no longer describe the live recognition path
- Show the recognized English text, translated Yoruba text, and audio player as before
