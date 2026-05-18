# Hidden Gemini Fallback Design

## Goal

Improve recognition robustness on difficult Braille images without changing the visible UI.

## Approach

- Keep the local OpenCV + CNN pipeline as the primary recognizer.
- Evaluate the local result quality after inference.
- If the local result is weak and `GEMINI_API_KEY` is configured, send the uploaded image to Gemini Vision.
- Use Gemini's returned English text as the recognized text for the rest of the pipeline.
- Continue with the existing offline Yoruba translation and eSpeak TTS steps.

## Weak-result rules

Trigger fallback when any of these are true:

- no cells detected
- local model was not used
- reconstructed text is empty
- `?` ratio in visible text is above the threshold
- average confidence is below the threshold

## User experience

- No UI switch
- No visible mention of whether Gemini was used
- Same text and audio outputs as before

## Failure behavior

- If `GEMINI_API_KEY` is missing, keep the local text
- If Gemini request fails, keep the local text
- If Gemini returns empty text, keep the local text
- No request should crash because of the fallback path
