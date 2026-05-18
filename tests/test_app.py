from io import BytesIO

from braille_system.gemini_fallback import GeminiRecognitionError
from braille_system.translation import GeminiTranslationError
from braille_system.tts import SpitchSynthesisError
from braille_system.translation import TranslationResult


def test_home_page_loads():
    from app import app

    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Upload Braille Image" in response.data


def test_upload_route_requires_file():
    from app import app

    client = app.test_client()
    response = client.post("/predict", data={}, content_type="multipart/form-data")
    assert response.status_code == 400


def test_audio_route_returns_404_for_missing_file():
    from app import app

    client = app.test_client()
    response = client.get("/audio/missing.mp3")
    assert response.status_code == 404


def test_upload_route_accepts_image(monkeypatch):
    from app import app

    captured = {}

    def fake_speech(_text, output_path, lang="yo"):
        captured["text"] = _text
        captured["lang"] = lang
        output_path.write_bytes(b"fake-audio")
        return output_path

    monkeypatch.setattr("app.synthesize_text_to_speech", fake_speech)
    monkeypatch.setattr("app.recognize_braille_with_gemini", lambda path: "demo output")
    monkeypatch.setattr(
        "app.translate_english_to_yoruba",
        lambda text: TranslationResult(
            source_text=text,
            translated_text="eyi ni idanwo",
            used_translation=True,
        ),
    )

    client = app.test_client()
    response = client.post(
        "/predict",
        data={"image": (BytesIO(b"fake-image-bytes"), "sample.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"demo output" in response.data
    assert b"eyi ni idanwo" in response.data
    assert b"Listen to audio output" in response.data
    assert b"Gemini" not in response.data
    assert captured == {"text": "eyi ni idanwo", "lang": "yo"}


def test_upload_route_falls_back_to_english_audio_when_translation_fails(monkeypatch):
    from app import app
    monkeypatch.setattr("app.recognize_braille_with_gemini", lambda path: "demo output")
    monkeypatch.setattr(
        "app.translate_english_to_yoruba",
        lambda text: (_ for _ in ()).throw(GeminiTranslationError("translation unavailable")),
    )

    client = app.test_client()
    response = client.post(
        "/predict",
        data={"image": (BytesIO(b"fake-image-bytes"), "sample.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 502
    assert b"Processing failed" in response.data
    assert b"translation unavailable" in response.data
    assert b"Try again" in response.data


def test_upload_route_rejects_non_image_extension():
    from app import app

    client = app.test_client()
    response = client.post(
        "/predict",
        data={"image": (BytesIO(b"plain-text"), "notes.txt")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400


def test_upload_route_returns_error_when_gemini_recognition_fails(monkeypatch):
    from app import app

    monkeypatch.setattr(
        "app.recognize_braille_with_gemini",
        lambda path: (_ for _ in ()).throw(GeminiRecognitionError("service unavailable")),
    )

    client = app.test_client()
    response = client.post(
        "/predict",
        data={"image": (BytesIO(b"fake-image-bytes"), "sample.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 502
    assert b"Processing failed" in response.data
    assert b"service unavailable" in response.data


def test_upload_route_returns_error_when_speech_synthesis_fails(monkeypatch):
    from app import app

    monkeypatch.setattr("app.recognize_braille_with_gemini", lambda path: "good morning")
    monkeypatch.setattr(
        "app.translate_english_to_yoruba",
        lambda text: TranslationResult(
            source_text=text,
            translated_text="e kaaro",
            used_translation=True,
        ),
    )
    monkeypatch.setattr(
        "app.synthesize_text_to_speech",
        lambda _text, output_path, lang="yo": (_ for _ in ()).throw(SpitchSynthesisError("tts unavailable")),
    )

    client = app.test_client()
    response = client.post(
        "/predict",
        data={"image": (BytesIO(b"fake-image-bytes"), "sample.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 502
    assert b"Processing failed" in response.data
    assert b"tts unavailable" in response.data


def test_home_page_includes_loading_state_markup():
    from app import app

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"processing-overlay" in response.data
    assert b"Processing your Braille image" in response.data
    assert b"Gemini" not in response.data
