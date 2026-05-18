# Offline Translation Design

## Goal

Replace the online English-to-Yoruba translator with a fully offline translation module so the Braille-to-Speech prototype no longer depends on internet access during inference.

## Approved Flow

`Braille image -> English text -> offline English-to-Yoruba translator -> eSpeak audio output`

## Scope

- Keep the Braille recognition pipeline unchanged.
- Replace `deep-translator` with a local translation module.
- Use deterministic phrase mapping first, then word-by-word mapping, then simple cleanup.
- Preserve audio generation through `eSpeak`.
- Never block on network access.

## Translation Strategy

- First check an exact phrase dictionary for common short expressions.
- If no exact phrase match exists, split the sentence into tokens and translate word-by-word using a built-in dictionary.
- Preserve punctuation and spacing.
- If a word has no Yoruba mapping, keep the English token instead of failing.
- Mark translation as used when at least one phrase or token is translated.

## Error Handling

- Empty input returns empty output.
- Unknown words stay in English.
- If nothing is translated, the app falls back to English audio.
- The translation module must not perform network calls or import online translation libraries.

## Testing

- Add unit tests for exact phrase translation, mixed known/unknown token translation, punctuation preservation, and no-network fallback behavior.
- Keep app integration tests verifying Yoruba audio is used when offline translation succeeds and English audio is used when no translation occurs.
