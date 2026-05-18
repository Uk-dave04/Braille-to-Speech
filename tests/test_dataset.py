from pathlib import Path

import cv2
import numpy as np

from braille_system.modeling.dataset import collect_image_paths, collect_image_paths_from_roots
from braille_system.modeling.train import load_dataset


def test_collect_image_paths_reads_class_directories(tmp_path: Path):
    class_dir = tmp_path / "100000"
    class_dir.mkdir()
    (class_dir / "sample.png").write_bytes(b"demo")

    items = collect_image_paths(tmp_path)

    assert items[0][1] == "100000"


def test_load_dataset_returns_images_labels_and_class_names(tmp_path: Path):
    class_a = tmp_path / "100000"
    class_b = tmp_path / "110000"
    class_a.mkdir()
    class_b.mkdir()

    image_a = np.full((12, 12), 255, dtype=np.uint8)
    image_b = np.zeros((12, 12), dtype=np.uint8)
    cv2.imwrite(str(class_a / "a.png"), image_a)
    cv2.imwrite(str(class_b / "b.png"), image_b)

    x, y, label_names = load_dataset(tmp_path, image_size=(16, 16))

    assert x.shape == (2, 16, 16, 1)
    assert y.shape == (2, 2)
    assert label_names == ["100000", "110000"]


def test_collect_image_paths_from_multiple_roots_merges_samples(tmp_path: Path):
    root_a = tmp_path / "dataset_a"
    root_b = tmp_path / "dataset_b"
    (root_a / "100000").mkdir(parents=True)
    (root_b / "110000").mkdir(parents=True)
    (root_a / "100000" / "a.png").write_bytes(b"demo")
    (root_b / "110000" / "b.png").write_bytes(b"demo")

    items = collect_image_paths_from_roots([root_a, root_b])

    assert len(items) == 2
    assert {label for _, label in items} == {"100000", "110000"}


def test_load_dataset_accepts_multiple_roots(tmp_path: Path):
    root_a = tmp_path / "dataset_a"
    root_b = tmp_path / "dataset_b"
    class_a = root_a / "100000"
    class_b = root_b / "110000"
    class_a.mkdir(parents=True)
    class_b.mkdir(parents=True)

    image_a = np.full((12, 12), 255, dtype=np.uint8)
    image_b = np.zeros((12, 12), dtype=np.uint8)
    cv2.imwrite(str(class_a / "a.png"), image_a)
    cv2.imwrite(str(class_b / "b.png"), image_b)

    x, y, label_names = load_dataset([root_a, root_b], image_size=(16, 16))

    assert x.shape == (2, 16, 16, 1)
    assert y.shape == (2, 2)
    assert label_names == ["100000", "110000"]
