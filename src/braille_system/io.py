from pathlib import Path

from config import AUDIO_DIR, UPLOAD_DIR


def ensure_runtime_dirs(_base_dir: Path) -> dict[str, Path]:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    return {"uploads": UPLOAD_DIR, "audio": AUDIO_DIR}
