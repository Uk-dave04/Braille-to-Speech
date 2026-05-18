import os
from pathlib import Path

DEFAULT_SPITCH_VOICE = "sade"


class SpitchSynthesisError(RuntimeError):
    """Raised when Spitch cannot synthesize usable audio."""


def build_audio_output_path(audio_dir: Path, stem: str) -> Path:
    return audio_dir / f"{stem}.wav"


def synthesize_text_to_speech(text: str, output_path: Path, lang: str = "yo") -> Path:
    api_key = os.getenv("SPITCH_API_KEY", "").strip()
    if not api_key:
        raise SpitchSynthesisError("SPITCH_API_KEY is not configured.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from spitch import Spitch

        client = Spitch(api_key=api_key)
        response = client.speech.generate(
            text=text,
            language=lang,
            voice=DEFAULT_SPITCH_VOICE,
            format="wav",
        )
        audio_bytes = response.read()
    except Exception as exc:
        raise SpitchSynthesisError(str(exc)) from exc

    output_path.write_bytes(audio_bytes)
    return output_path
