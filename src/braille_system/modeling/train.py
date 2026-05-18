from pathlib import Path
import os
import json

import cv2
import numpy as np
from sklearn.model_selection import train_test_split

from config import MODEL_PATH, PROCESSED_DATASET_DIR
from .dataset import collect_image_paths, collect_image_paths_from_roots
from .model import build_braille_cnn


def resolve_dataset_roots(root_dirs: Path | list[Path] | None = None) -> list[Path]:
    if root_dirs is None:
        env_value = os.getenv("BRAILLE_DATASET_DIRS", "").strip()
        if env_value:
            return [Path(part) for part in env_value.split(os.pathsep) if part.strip()]
        return [PROCESSED_DATASET_DIR]

    if isinstance(root_dirs, Path):
        return [root_dirs]

    return list(root_dirs)


def load_dataset(root_dir: Path | list[Path], image_size: tuple[int, int] = (32, 32)):
    try:
        from tensorflow import keras
    except ImportError as exc:
        raise RuntimeError(
            "TensorFlow is required to load labels as categorical tensors."
        ) from exc

    roots = resolve_dataset_roots(root_dir)
    samples = (
        collect_image_paths(roots[0])
        if len(roots) == 1
        else collect_image_paths_from_roots(roots)
    )
    if not samples:
        raise ValueError(f"No PNG training samples found in {roots}")

    label_names = sorted({label for _, label in samples})
    label_to_index = {label: idx for idx, label in enumerate(label_names)}

    images = []
    labels = []

    for image_path, label in samples:
        image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if image is None:
            continue

        resized = cv2.resize(image, image_size)
        normalized = resized.astype("float32") / 255.0
        images.append(normalized[..., np.newaxis])
        labels.append(label_to_index[label])

    if not images:
        raise ValueError("Dataset paths were found, but no images could be loaded.")

    x = np.array(images)
    y = keras.utils.to_categorical(labels, num_classes=len(label_names))
    return x, y, label_names


def split_train_validation(x, y, test_size: float = 0.2, random_state: int = 42):
    class_indices = y.argmax(axis=1)
    class_counts = np.bincount(class_indices)
    n_samples = len(x)
    n_classes = int(np.count_nonzero(class_counts))
    n_test = int(np.ceil(n_samples * test_size)) if isinstance(test_size, float) else int(test_size)
    n_train = n_samples - n_test
    use_stratify = (
        np.all(class_counts[class_counts > 0] >= 2)
        and n_test >= n_classes
        and n_train >= n_classes
    )

    return train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=class_indices if use_stratify else None,
    )


def compute_class_weights(y) -> dict[int, float]:
    class_indices = y.argmax(axis=1)
    class_counts = np.bincount(class_indices)
    nonzero_classes = np.nonzero(class_counts)[0]
    total_samples = len(class_indices)
    num_classes = len(nonzero_classes)

    weights: dict[int, float] = {}
    for class_id in nonzero_classes:
        weights[int(class_id)] = total_samples / (num_classes * class_counts[class_id])
    return weights


def main():
    try:
        from tensorflow import keras
    except ImportError as exc:
        raise RuntimeError(
            "TensorFlow is required to train the Braille CNN."
        ) from exc

    dataset_dirs = resolve_dataset_roots()
    x, y, label_names = load_dataset(dataset_dirs)

    x_train, x_val, y_train, y_val = split_train_validation(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = build_braille_cnn((32, 32, 1), len(label_names))
    callbacks = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(str(MODEL_PATH), save_best_only=True),
    ]

    use_class_weights = False
    model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=25,
        batch_size=32,
        callbacks=callbacks,
        class_weight=compute_class_weights(y_train) if use_class_weights else None,
    )
    MODEL_PATH.with_suffix(".labels.json").write_text(
        json.dumps(label_names, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
