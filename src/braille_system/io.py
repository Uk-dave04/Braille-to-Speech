from pathlib import Path


def ensure_runtime_dirs(base_dir: Path) -> dict[str, Path]:
    uploads = base_dir / "uploads"
    audio = base_dir / "outputs" / "audio"
    uploads.mkdir(parents=True, exist_ok=True)
    audio.mkdir(parents=True, exist_ok=True)
    return {"uploads": uploads, "audio": audio}
