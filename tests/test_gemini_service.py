from pathlib import Path

import pytest

from braille_system.gemini_fallback import GeminiRecognitionError, recognize_braille_with_gemini


def test_recognize_braille_with_gemini_returns_text_when_request_succeeds(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"demo")

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        "braille_system.gemini_fallback.request_gemini_braille_text",
        lambda image_path, api_key=None, model_name="gemini-2.5-flash", prompt=None: "hello world",
    )

    assert recognize_braille_with_gemini(image_path) == "hello world"


def test_recognize_braille_with_gemini_raises_when_api_key_is_missing(tmp_path: Path):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"demo")

    with pytest.raises(GeminiRecognitionError, match="API key"):
        recognize_braille_with_gemini(image_path)


def test_recognize_braille_with_gemini_raises_when_gemini_returns_empty_text(
    monkeypatch,
    tmp_path: Path,
):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"demo")

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        "braille_system.gemini_fallback.request_gemini_braille_text",
        lambda image_path, api_key=None, model_name="gemini-2.5-flash", prompt=None: "   ",
    )

    with pytest.raises(GeminiRecognitionError, match="empty text"):
        recognize_braille_with_gemini(image_path)


def test_recognize_braille_with_gemini_wraps_transport_errors(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"demo")

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def fail(*args, **kwargs):
        raise RuntimeError("service unavailable")

    monkeypatch.setattr("braille_system.gemini_fallback.request_gemini_braille_text", fail)

    with pytest.raises(GeminiRecognitionError, match="service unavailable"):
        recognize_braille_with_gemini(image_path)


def test_recognize_braille_with_gemini_retries_and_falls_back_on_503(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"demo")

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr("braille_system.gemini_fallback.time.sleep", lambda seconds: None)

    calls: list[str] = []

    def flaky(image_path, api_key=None, model_name="gemini-2.5-flash", prompt=None):
        calls.append(model_name)
        if len(calls) < 3:
            raise RuntimeError(
                "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'high demand', 'status': 'UNAVAILABLE'}}"
            )
        return "recognized text"

    monkeypatch.setattr("braille_system.gemini_fallback.request_gemini_braille_text", flaky)

    assert recognize_braille_with_gemini(image_path) == "recognized text"
    assert calls == ["gemini-2.5-flash", "gemini-2.5-flash", "gemini-2.5-flash"]


def test_recognize_braille_with_gemini_uses_second_prompt_after_empty_response(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"demo")

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr("braille_system.gemini_fallback.time.sleep", lambda seconds: None)
    monkeypatch.setattr(
        "braille_system.gemini_fallback.build_gemini_ready_image",
        lambda path: path,
    )

    prompts: list[str] = []

    def by_prompt(image_path, api_key=None, model_name="gemini-2.5-flash", prompt=None):
        prompts.append(prompt or "")
        if len(prompts) == 1:
            return ""
        return "partial readable text"

    monkeypatch.setattr("braille_system.gemini_fallback.request_gemini_braille_text", by_prompt)

    assert recognize_braille_with_gemini(image_path) == "partial readable text"
    assert len(prompts) >= 2
