from pathlib import Path

import cv2
import numpy as np


def load_inference_model(model_path: Path):
    try:
        from tensorflow import keras
    except ImportError as exc:
        raise RuntimeError(
            "TensorFlow is required to load the Braille inference model."
        ) from exc

    return keras.models.load_model(model_path)


def prepare_cell_for_model(cell_image: np.ndarray) -> np.ndarray:
    resized = cv2.resize(cell_image, (32, 32))
    normalized = resized.astype("float32") / 255.0
    return normalized[np.newaxis, ..., np.newaxis]


def prepare_cells_for_model(cell_images: list[np.ndarray]) -> np.ndarray:
    if not cell_images:
        return np.empty((0, 32, 32, 1), dtype="float32")
    prepared = [prepare_cell_for_model(cell)[0] for cell in cell_images]
    return np.stack(prepared, axis=0)


def predict_braille_pattern(model, cell_image: np.ndarray, class_names: list[str]) -> tuple[str, float]:
    batch = prepare_cell_for_model(cell_image)
    scores = model.predict(batch, verbose=0)[0]
    index = int(scores.argmax())
    return class_names[index], float(scores[index])


def predict_braille_patterns(
    model,
    cell_images: list[np.ndarray],
    class_names: list[str],
) -> list[tuple[str, float]]:
    if not cell_images:
        return []

    batch = prepare_cells_for_model(cell_images)
    scores = model.predict(batch, verbose=0)
    expected_classes = scores.shape[1]
    if len(class_names) != expected_classes:
        raise RuntimeError(
            f"Label count mismatch: model outputs {expected_classes} classes but "
            f"{len(class_names)} class names were discovered."
        )
    predictions: list[tuple[str, float]] = []
    for score_vector in scores:
        index = int(score_vector.argmax())
        predictions.append((class_names[index], float(score_vector[index])))
    return predictions
