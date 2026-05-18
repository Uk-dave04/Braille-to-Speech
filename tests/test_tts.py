from pathlib import Path
import sys
import types

import pytest

from braille_system.tts import (
    SpitchSynthesisError,
    build_audio_output_path,
    synthesize_text_to_speech,
)


def test_build_audio_output_path_uses_wav_suffix(tmp_path: Path):
    result = build_audio_output_path(tmp_path, "demo")
    assert result.suffix == ".wav"


def test_synthesize_text_to_speech_raises_when_spitch_key_is_missing(tmp_path: Path):
    with pytest.raises(SpitchSynthesisError, match="SPITCH_API_KEY"):
        synthesize_text_to_speech("bawo ni", tmp_path / "demo.wav", lang="yo")


def test_synthesize_text_to_speech_writes_audio_from_spitch_response(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SPITCH_API_KEY", "test-key")

    class FakeResponse:
        def read(self):
            return b"RIFFdemo"

    class FakeSpeech:
        def generate(self, **kwargs):
            self.kwargs = kwargs
            return FakeResponse()

    fake_speech = FakeSpeech()

    class FakeClient:
        def __init__(self, api_key=None):
            self.api_key = api_key
            self.speech = fake_speech

    monkeypatch.setitem(sys.modules, "spitch", types.SimpleNamespace(Spitch=FakeClient))

    output_path = tmp_path / "demo.wav"
    result = synthesize_text_to_speech("bawo ni", output_path, lang="yo")

    assert result == output_path
    assert output_path.read_bytes() == b"RIFFdemo"
    assert fake_speech.kwargs["text"] == "bawo ni"
    assert fake_speech.kwargs["language"] == "yo"
    assert fake_speech.kwargs["voice"] == "sade"
    assert fake_speech.kwargs["format"] == "wav"


def test_synthesize_text_to_speech_wraps_spitch_errors(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SPITCH_API_KEY", "test-key")

    class FakeSpeech:
        def generate(self, **kwargs):
            raise RuntimeError("spitch down")

    class FakeClient:
        def __init__(self, api_key=None):
            self.speech = FakeSpeech()

    monkeypatch.setitem(sys.modules, "spitch", types.SimpleNamespace(Spitch=FakeClient))

    with pytest.raises(SpitchSynthesisError, match="spitch down"):
        synthesize_text_to_speech("bawo ni", tmp_path / "demo.wav", lang="yo")
