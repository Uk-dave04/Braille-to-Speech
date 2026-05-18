# Gemini Translation and Spitch TTS Design

## Goal

Improve the quality of Yoruba output by replacing the limited local translation dictionary and robotic offline speech path.

## Architecture

- Gemini Vision reads the uploaded Braille image and returns English text.
- Gemini translates the English text into Yoruba.
- Spitch synthesizes Yoruba audio from the translated text.
- The app returns an error if any of these cloud stages fail.

## Error handling

- If Gemini recognition fails, return `502`
- If Gemini translation fails, return `502`
- If Spitch speech synthesis fails, return `502`
- Do not silently fall back to the old dictionary translator or eSpeak in the live app

## UI behavior

- Keep the same upload and result screens
- Show recognized English text, translated Yoruba text, and audio player
- Remove messaging that implies offline translation or offline speech in the live app
