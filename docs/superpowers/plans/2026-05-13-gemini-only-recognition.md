# Gemini-Only Recognition Plan

1. Replace the app's image-to-text stage with a strict Gemini service call.
2. Add a small Gemini service API that raises a dedicated error when the API key is missing, Gemini is unreachable, or Gemini returns empty text.
3. Update the Flask route to return a `502` error payload for Gemini recognition failures.
4. Remove local recognition metrics from the result page.
5. Add tests for successful Gemini recognition and error cases.
6. Document permanent Windows API-key setup and the Gemini-only recognition flow.
