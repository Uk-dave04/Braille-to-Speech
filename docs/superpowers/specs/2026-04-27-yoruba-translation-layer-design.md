# Yoruba Translation Layer Design

## Goal

Extend the current Braille-to-Speech prototype so that Braille images are recognized as English text first, then translated online into Yoruba text before speech is generated.

## Approved flow

`Braille image -> English text -> online English-to-Yoruba translation -> Yoruba TTS -> audio output`

## Scope

- Keep the existing Braille recognition pipeline unchanged
- Add a small translation service between recognition and TTS
- Show both the recognized English text and translated Yoruba text on the result page
- Fall back to English speech if translation is unavailable

## Design choices

- Use a free online translator library instead of a paid API for the MVP
- Keep translation logic isolated in its own module so we can swap providers later
- Preserve app stability by treating translation as optional enhancement, not a hard dependency for recognition

## Error handling

- If translation succeeds, synthesize Yoruba speech from the translated text
- If translation fails or the dependency is unavailable, use the recognized English text for speech and surface a fallback message in the UI
- If TTS fails, still render the text outputs and recognition metadata
