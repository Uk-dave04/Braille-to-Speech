from pathlib import Path

import cv2
import numpy as np
import pytest

from braille_system.pipeline import RecognitionResult, clear_model_cache, process_uploaded_braille_image


def test_process_uploaded_braille_image_returns_placeholder_result(tmp_path: Path):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((20, 20, 3), 255, dtype=np.uint8))

    result = process_uploaded_braille_image(
        image_path,
        model_path=tmp_path / "missing.keras",
        dataset_dir=tmp_path / "missing_dataset",
        debug_root=tmp_path / "debug",
    )

    assert isinstance(result, RecognitionResult)
    assert result.text == "demo output"
    assert result.confidences == []


def test_process_uploaded_braille_image_runs_real_orchestration(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((40, 40, 3), 255, dtype=np.uint8))

    model_path = tmp_path / "braille_cnn.keras"
    model_path.write_bytes(b"model")
    dataset_dir = tmp_path / "labels"
    (dataset_dir / "100000").mkdir(parents=True)
    (dataset_dir / "110000").mkdir(parents=True)

    loaded = {"count": 0}

    def fake_load(_path):
        loaded["count"] += 1
        return object()

    monkeypatch.setattr("braille_system.pipeline.load_inference_model", fake_load)
    monkeypatch.setattr(
        "braille_system.pipeline.preprocess_braille_image",
        lambda image: np.full((40, 40), 255, dtype=np.uint8),
    )
    monkeypatch.setattr(
        "braille_system.pipeline.extract_candidate_cells",
        lambda image: [(0, 0, 10, 10), (20, 0, 10, 10)],
    )

    monkeypatch.setattr(
        "braille_system.pipeline.predict_braille_patterns",
        lambda model, crops, class_names: [("100000", 0.9), ("110000", 0.8)],
    )
    monkeypatch.setattr("braille_system.pipeline._save_debug_artifacts", lambda *args, **kwargs: {})

    clear_model_cache()

    result = process_uploaded_braille_image(
        image_path,
        model_path=model_path,
        dataset_dir=dataset_dir,
    )

    assert result.text == "ab"
    assert result.confidences == [0.9, 0.8]
    assert result.cells_detected == 2
    assert loaded["count"] == 1


def test_process_uploaded_braille_image_reuses_cached_model(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((40, 40, 3), 255, dtype=np.uint8))

    model_path = tmp_path / "braille_cnn.keras"
    model_path.write_bytes(b"model")
    dataset_dir = tmp_path / "labels"
    (dataset_dir / "100000").mkdir(parents=True)

    loaded = {"count": 0}

    def fake_load(_path):
        loaded["count"] += 1
        return object()

    monkeypatch.setattr("braille_system.pipeline.load_inference_model", fake_load)
    monkeypatch.setattr(
        "braille_system.pipeline.preprocess_braille_image",
        lambda image: np.full((20, 20), 255, dtype=np.uint8),
    )
    monkeypatch.setattr(
        "braille_system.pipeline.extract_candidate_cells",
        lambda image: [(0, 0, 10, 10)],
    )
    monkeypatch.setattr(
        "braille_system.pipeline.predict_braille_patterns",
        lambda model, crops, class_names: [("100000", 0.95)],
    )
    monkeypatch.setattr("braille_system.pipeline._save_debug_artifacts", lambda *args, **kwargs: {})

    clear_model_cache()
    process_uploaded_braille_image(image_path, model_path=model_path, dataset_dir=dataset_dir)
    process_uploaded_braille_image(image_path, model_path=model_path, dataset_dir=dataset_dir)

    assert loaded["count"] == 1


def test_process_uploaded_braille_image_skips_debug_artifacts_by_default(monkeypatch, tmp_path: Path):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((20, 20, 3), 255, dtype=np.uint8))

    monkeypatch.setattr(
        "braille_system.pipeline.preprocess_braille_image",
        lambda image: np.full((20, 20), 255, dtype=np.uint8),
    )
    monkeypatch.setattr(
        "braille_system.pipeline.extract_candidate_cells",
        lambda image: [],
    )

    called = {"count": 0}

    def fake_save(*args, **kwargs):
        called["count"] += 1
        return {"original": tmp_path / "x.png"}

    monkeypatch.setattr("braille_system.pipeline._save_debug_artifacts", fake_save)

    result = process_uploaded_braille_image(
        image_path,
        model_path=tmp_path / "missing.keras",
        dataset_dir=tmp_path / "missing_dataset",
        debug_root=tmp_path / "debug",
    )

    assert result.debug_artifacts == {}
    assert called["count"] == 0


def test_process_uploaded_braille_image_uses_multiple_dataset_roots_from_env(
    monkeypatch,
    tmp_path: Path,
):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((40, 40, 3), 255, dtype=np.uint8))

    model_path = tmp_path / "braille_cnn.keras"
    model_path.write_bytes(b"model")
    root_a = tmp_path / "dataset_a"
    root_b = tmp_path / "dataset_b"
    (root_a / "100000").mkdir(parents=True)
    (root_b / "111111").mkdir(parents=True)

    captured_class_names: list[str] = []

    monkeypatch.setenv("BRAILLE_DATASET_DIRS", f"{root_a};{root_b}")
    monkeypatch.setattr("braille_system.pipeline.load_inference_model", lambda _path: object())
    monkeypatch.setattr(
        "braille_system.pipeline.preprocess_braille_image",
        lambda image: np.full((20, 20), 255, dtype=np.uint8),
    )
    monkeypatch.setattr(
        "braille_system.pipeline.extract_candidate_cells",
        lambda image: [(0, 0, 10, 10)],
    )

    def fake_predict(model, crops, class_names):
        captured_class_names.extend(class_names)
        return [("100000", 0.95)]

    monkeypatch.setattr("braille_system.pipeline.predict_braille_patterns", fake_predict)
    monkeypatch.setattr("braille_system.pipeline._save_debug_artifacts", lambda *args, **kwargs: {})

    clear_model_cache()
    result = process_uploaded_braille_image(
        image_path,
        model_path=model_path,
        dataset_dir=None,
    )

    assert result.text == "a"
    assert captured_class_names == ["100000", "111111"]


def test_process_uploaded_braille_image_prefers_model_label_file(
    monkeypatch,
    tmp_path: Path,
):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), np.full((40, 40, 3), 255, dtype=np.uint8))

    model_path = tmp_path / "braille_cnn.keras"
    model_path.write_bytes(b"model")
    model_labels_path = model_path.with_suffix(".labels.json")
    model_labels_path.write_text('["100000", "111111"]', encoding="utf-8")
    dataset_dir = tmp_path / "labels"
    (dataset_dir / "100000").mkdir(parents=True)

    captured_class_names: list[str] = []

    monkeypatch.setattr("braille_system.pipeline.load_inference_model", lambda _path: object())
    monkeypatch.setattr(
        "braille_system.pipeline.preprocess_braille_image",
        lambda image: np.full((20, 20), 255, dtype=np.uint8),
    )
    monkeypatch.setattr(
        "braille_system.pipeline.extract_candidate_cells",
        lambda image: [(0, 0, 10, 10)],
    )

    def fake_predict(model, crops, class_names):
        captured_class_names.extend(class_names)
        return [("100000", 0.95)]

    monkeypatch.setattr("braille_system.pipeline.predict_braille_patterns", fake_predict)
    monkeypatch.setattr("braille_system.pipeline._save_debug_artifacts", lambda *args, **kwargs: {})

    clear_model_cache()
    result = process_uploaded_braille_image(
        image_path,
        model_path=model_path,
        dataset_dir=dataset_dir,
    )

    assert result.text == "a"
    assert captured_class_names == ["100000", "111111"]
