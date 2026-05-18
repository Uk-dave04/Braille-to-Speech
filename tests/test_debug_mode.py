from pathlib import Path

import cv2
import numpy as np

from braille_system.pipeline import process_uploaded_braille_image


def test_process_uploaded_braille_image_saves_debug_artifacts(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((40, 40, 3), 255, dtype=np.uint8))

    model_path = tmp_path / "braille_cnn.keras"
    model_path.write_bytes(b"model")
    dataset_dir = tmp_path / "labels"
    (dataset_dir / "100000").mkdir(parents=True)

    monkeypatch.setattr("braille_system.pipeline.load_inference_model", lambda path: object())
    monkeypatch.setattr(
        "braille_system.pipeline.preprocess_braille_image",
        lambda image: np.full((40, 40), 255, dtype=np.uint8),
    )
    monkeypatch.setattr(
        "braille_system.pipeline.extract_candidate_cells",
        lambda image: [(0, 0, 10, 10)],
    )
    monkeypatch.setattr(
        "braille_system.pipeline.predict_braille_patterns",
        lambda model, crops, class_names: [("100000", 0.9)],
    )

    result = process_uploaded_braille_image(
        image_path,
        model_path=model_path,
        dataset_dir=dataset_dir,
        debug_root=tmp_path / "debug",
        save_debug_artifacts=True,
    )

    assert result.debug_artifacts["original"].exists()
    assert result.debug_artifacts["binary"].exists()
    assert result.debug_artifacts["overlay"].exists()
    assert result.model_used is True
