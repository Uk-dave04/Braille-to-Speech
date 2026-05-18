import os
from dataclasses import dataclass
import time

from google import genai

from .utils import normalize_text_for_tts

DEFAULT_GEMINI_TRANSLATION_MODEL = "gemini-2.0-flash"
FALLBACK_GEMINI_TRANSLATION_MODEL = "gemini-2.5-flash"
MAX_ATTEMPTS_PER_MODEL = 2
RETRY_DELAY_SECONDS = 1.0
TRANSLATION_PROMPT_TEMPLATE = (
    "Translate the following English text into natural, fully diacritized Yoruba suitable for text-to-speech. "
    "Preserve Yoruba tone marks and underdots where needed. Return only the Yoruba translation with no explanation "
    "and no surrounding quotes.\n\n"
    "English:\n{text}"
)


class GeminiTranslationError(RuntimeError):
    """Raised when Gemini cannot provide usable Yoruba translation."""


def _is_transient_gemini_overload_error(message: str) -> bool:
    upper_message = message.upper()
    return "503" in upper_message and "UNAVAILABLE" in upper_message


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    used_translation: bool
    fallback_reason: str | None = None


def request_gemini_yoruba_translation(
    text: str,
    api_key: str | None = None,
    model_name: str = DEFAULT_GEMINI_TRANSLATION_MODEL,
) -> str:
    resolved_api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
    if not resolved_api_key:
        raise GeminiTranslationError("Gemini API key is not configured.")

    try:
        client = genai.Client(api_key=resolved_api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=TRANSLATION_PROMPT_TEMPLATE.format(text=text),
        )
    except Exception as exc:
        raise GeminiTranslationError(str(exc)) from exc

    return " ".join((response.text or "").split())


def translate_english_to_yoruba(text: str) -> TranslationResult:
    normalized = normalize_text_for_tts(text)
    if not normalized:
        return TranslationResult(
            source_text="",
            translated_text="",
            used_translation=False,
        )

    last_error: Exception | None = None
    translated_text = ""
    for model_name in (DEFAULT_GEMINI_TRANSLATION_MODEL, FALLBACK_GEMINI_TRANSLATION_MODEL):
        for attempt in range(MAX_ATTEMPTS_PER_MODEL):
            try:
                translated_text = " ".join(
                    request_gemini_yoruba_translation(normalized, model_name=model_name).split()
                )
            except GeminiTranslationError as exc:
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
                raise GeminiTranslationError(str(exc)) from exc

            if translated_text:
                return TranslationResult(
                    source_text=normalized,
                    translated_text=translated_text,
                    used_translation=True,
                )
            raise GeminiTranslationError("Gemini returned empty text.")

    if last_error is not None:
        raise GeminiTranslationError(str(last_error)) from last_error
    raise GeminiTranslationError("Gemini translation failed.")
