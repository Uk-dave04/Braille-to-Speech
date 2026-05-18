import json
from pathlib import Path

import cv2
import numpy as np

from braille_system.modeling.prepare_character_dataset import (
    decimal_label_to_pattern,
    parse_annotation_line,
    prepare_character_dataset,
)


def test_parse_annotation_line_returns_box_and_label():
    annotation = "48,5,82,5,82,58,48,58,26,"

    parsed = parse_annotation_line(annotation)

    assert parsed["label"] == "26"
    assert parsed["bbox"] == (48, 5, 82, 58)


def test_decimal_label_to_pattern_uses_six_dot_binary_order():
    assert decimal_label_to_pattern("1") == "100000"
    assert decimal_label_to_pattern("3") == "110000"
    assert decimal_label_to_pattern("63") == "111111"


def test_prepare_character_dataset_crops_images_and_writes_summary(tmp_path: Path):
    raw_root = tmp_path / "raw"
    image_dir = raw_root / "train"
    image_dir.mkdir(parents=True)

    image = np.full((80, 100, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (10, 10), (40, 60), (0, 0, 0), -1)
    image_path = image_dir / "sample.jpg"
    cv2.imwrite(str(image_path), image)
    (image_dir / "sample.txt").write_text("10,10,40,10,40,60,10,60,26,\n")

    output_dir = tmp_path / "processed"
    summary_path = tmp_path / "summary.json"

    prepare_character_dataset(raw_root, output_dir, summary_path)

    cropped_files = list((output_dir / "010110").glob("*.png"))
    assert len(cropped_files) == 1

    summary = json.loads(summary_path.read_text())
    assert summary["total_crops"] == 1
    assert summary["class_counts"]["010110"] == 1
