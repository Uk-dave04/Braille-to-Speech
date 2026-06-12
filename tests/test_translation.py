from pathlib import Path

import pytest

from braille_system.translation import (
    GeminiTranslationError,
    TRANSLATION_PROMPT_TEMPLATE,
    TranslationResult,
    translate_english_to_yoruba,
)


def test_translate_english_to_yoruba_returns_structured_result(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        "braille_system.translation.request_gemini_yoruba_translation",
        lambda text, api_key=None, model_name="gemini-2.0-flash": "e kaaro",
    )

    result = translate_english_to_yoruba("good morning")

    assert isinstance(result, TranslationResult)
    assert result.source_text == "good morning"
    assert result.translated_text == "e kaaro"
    assert result.used_translation is True
    assert result.fallback_reason is None


def test_translation_prompt_requests_fully_diacritized_yoruba():
    prompt = TRANSLATION_PROMPT_TEMPLATE.format(text="good morning")

    assert "fully diacritized Yoruba" in prompt
    assert "text-to-speech" in prompt


def test_translate_english_to_yoruba_raises_when_api_key_is_missing():
    with pytest.raises(GeminiTranslationError, match="API key"):
        translate_english_to_yoruba("hello")


def test_translate_english_to_yoruba_raises_when_model_returns_empty_text(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        "braille_system.translation.request_gemini_yoruba_translation",
        lambda text, api_key=None, model_name="gemini-2.0-flash": "   ",
    )

    with pytest.raises(GeminiTranslationError, match="empty text"):
        translate_english_to_yoruba("hello")


def test_translate_english_to_yoruba_retries_and_falls_back_on_503(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr("braille_system.translation.time.sleep", lambda seconds: None)

    calls: list[str] = []

    def flaky(text, api_key=None, model_name="gemini-2.0-flash"):
        calls.append(model_name)
        if len(calls) < 3:
            raise RuntimeError(
                "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'high demand', 'status': 'UNAVAILABLE'}}"
            )
        return "e kaaro"

    monkeypatch.setattr("braille_system.translation.request_gemini_yoruba_translation", flaky)

    result = translate_english_to_yoruba("good morning")

    assert result.translated_text == "e kaaro"
    assert calls == ["gemini-2.0-flash", "gemini-2.0-flash", "gemini-2.0-flash"]


def test_translate_english_to_yoruba_retries_rate_limit_errors(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr("braille_system.translation.time.sleep", lambda seconds: None)

    calls = 0

    def flaky(text, api_key=None, model_name="gemini-2.0-flash"):
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError(
                "429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'quota exceeded', "
                "'status': 'RESOURCE_EXHAUSTED'}}"
            )
        return "e kaaro"

    monkeypatch.setattr("braille_system.translation.request_gemini_yoruba_translation", flaky)

    result = translate_english_to_yoruba("good morning")

    assert result.translated_text == "e kaaro"
    assert calls == 3
