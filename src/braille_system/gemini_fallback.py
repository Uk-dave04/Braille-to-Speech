import os
from pathlib import Path
import time

from PIL import Image, ImageOps

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
FALLBACK_GEMINI_MODEL = "gemini-2.0-flash"
MAX_ATTEMPTS_PER_MODEL = 2
RETRY_DELAY_SECONDS = 1.0
BRAILLE_PROMPT = (
    "You are reading a Braille image. Extract only the plain English text represented "
    "by the Braille dots. Return only the text itself with no explanation, no markdown, "
    "and no surrounding quotes. If the Braille is unreadable, return an empty string."
)
RELAXED_BRAILLE_PROMPT = (
    "Read this Braille image as carefully as you can and return any readable English text, "
    "even if partial. Return only the text itself with no explanation, no markdown, and no "
    "surrounding quotes. If nothing is readable, return an empty string."
)


class GeminiRecognitionError(RuntimeError):
    """Raised when Gemini cannot provide usable Braille text."""


def _is_transient_gemini_overload_error(message: str) -> bool:
    upper_message = message.upper()
    return "503" in upper_message and "UNAVAILABLE" in upper_message


def request_gemini_braille_text(
    image_path: Path,
    api_key: str | None = None,
    model_name: str = DEFAULT_GEMINI_MODEL,
    prompt: str = BRAILLE_PROMPT,
) -> str:
    try:
        from google import genai
    except ImportError as exc:
        raise GeminiRecognitionError(
            "google-genai is required for Gemini recognition support."
        ) from exc

    resolved_api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
    if not resolved_api_key:
        raise GeminiRecognitionError("Gemini API key is not configured.")

    try:
        client = genai.Client(api_key=resolved_api_key)
        uploaded_file = client.files.upload(file=str(image_path))
        response = client.models.generate_content(
            model=model_name,
            contents=[uploaded_file, prompt],
        )
    except Exception as exc:
        raise GeminiRecognitionError(str(exc)) from exc

    text = " ".join((response.text or "").split())
    return text


def build_gemini_ready_image(image_path: Path) -> Path:
    try:
        image = Image.open(image_path)
    except Exception:
        return image_path

    grayscale = ImageOps.grayscale(image)
    normalized = ImageOps.autocontrast(grayscale)
    upscaled = normalized.resize(
        (normalized.width * 2, normalized.height * 2),
        resample=Image.Resampling.LANCZOS,
    )
    enhanced_path = image_path.with_name(f"{image_path.stem}_gemini_enhanced.png")
    upscaled.save(enhanced_path)
    return enhanced_path


def recognize_braille_with_gemini(image_path: Path) -> str:
    last_error: Exception | None = None
    candidate_images = (
        (image_path, BRAILLE_PROMPT),
        (build_gemini_ready_image(image_path), RELAXED_BRAILLE_PROMPT),
    )
    for candidate_image_path, prompt in candidate_images:
        for model_name in (DEFAULT_GEMINI_MODEL, FALLBACK_GEMINI_MODEL):
            for attempt in range(MAX_ATTEMPTS_PER_MODEL):
                try:
                    text = request_gemini_braille_text(
                        candidate_image_path,
                        model_name=model_name,
                        prompt=prompt,
                    )
                except GeminiRecognitionError as exc:
                    if _is_transient_gemini_overload_error(str(exc)) and attempt < MAX_ATTEMPTS_PER_MODEL - 1:
                        time.sleep(RETRY_DELAY_SECONDS)
                        last_error = exc
                        continue
                    last_error = exc
                    break
                except Exception as exc:
                    if _is_transient_gemini_overload_error(str(exc)):
                        last_error = exc
                        if attempt < MAX_ATTEMPTS_PER_MODEL - 1:
                            time.sleep(RETRY_DELAY_SECONDS)
                            continue
                        break
                    raise GeminiRecognitionError(str(exc)) from exc

                text = " ".join(text.split())
                if text:
                    return text

    if last_error is not None:
        raise GeminiRecognitionError(str(last_error)) from last_error
    raise GeminiRecognitionError("Gemini returned empty text.")
