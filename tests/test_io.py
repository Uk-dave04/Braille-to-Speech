from pathlib import Path

from braille_system.io import ensure_runtime_dirs


def test_ensure_runtime_dirs_creates_expected_folders(tmp_path: Path):
    created = ensure_runtime_dirs(tmp_path)

    assert (tmp_path / "uploads").exists()
    assert (tmp_path / "outputs" / "audio").exists()
    assert created["uploads"] == tmp_path / "uploads"
    assert created["audio"] == tmp_path / "outputs" / "audio"
