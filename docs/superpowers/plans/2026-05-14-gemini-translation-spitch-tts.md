# Gemini Translation and Spitch TTS Plan

1. Replace the local translation dictionary with a Gemini translation service.
2. Replace the eSpeak wrapper with a Spitch synthesis service.
3. Update the Flask route so translation and TTS failures return `502` errors.
4. Add tests for successful translation, empty Gemini translation, missing Spitch key, and TTS service failures.
5. Add the `spitch` dependency and update setup docs for `SPITCH_API_KEY`.
