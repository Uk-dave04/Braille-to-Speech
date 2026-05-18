# Hidden Gemini Fallback Plan

1. Add a backend helper that scores the local recognition result and decides whether fallback is needed.
2. Add a Gemini request wrapper using the official `google-genai` Python client.
3. Integrate the helper into the Flask route before translation and TTS.
4. Keep the fallback invisible to the UI and preserve the existing page contract.
5. Add regression tests for:
   - good local result keeps local text
   - weak local result uses Gemini when configured
   - missing Gemini configuration falls back safely to local text
6. Update README setup instructions for `GEMINI_API_KEY`.
