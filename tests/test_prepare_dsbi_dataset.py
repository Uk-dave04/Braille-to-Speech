import json
from pathlib import Path

import cv2
import numpy as np

from braille_system.modeling.prepare_dsbi_dataset import (
    cell_annotation_to_pattern,
    parse_dsbi_annotation,
    prepare_dsbi_dataset,
)


def test_parse_dsbi_annotation_reads_lines_and_cells():
    annotation_text = "\n".join(
        [
            "0.80",
            "10 20 30 40",
            "15 25 35",
            "1 1 1 0 1 0 0 0",
        ]
    )

    parsed = parse_dsbi_annotation(annotation_text)

    assert parsed["angle"] == 0.80
    assert parsed["vertical_lines"] == [10, 20, 30, 40]
    assert parsed["horizontal_lines"] == [15, 25, 35]
    assert parsed["cells"][0] == {
        "row": 1,
        "col": 1,
        "dots": [1, 0, 1, 0, 0, 0],
    }


def test_cell_annotation_to_pattern_uses_annotation_order():
    assert cell_annotation_to_pattern([1, 0, 1, 0, 0, 0]) == "101000"


def test_prepare_dsbi_dataset_crops_cells_and_writes_summary(tmp_path: Path):
    raw_root = tmp_path / "raw"
    book_dir = raw_root / "Book"
    book_dir.mkdir(parents=True)

    image = np.full((80, 80, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (9, 14), (21, 36), (0, 0, 0), -1)
    image_path = book_dir / "sample+recto.jpg"
    cv2.imwrite(str(image_path), image)

    annotation_text = "\n".join(
        [
            "0.0",
            "10 20",
            "15 25 35",
            "1 1 1 0 1 0 0 0",
        ]
    )
    (book_dir / "sample+recto.txt").write_text(annotation_text)

    output_dir = tmp_path / "processed"
    summary_path = tmp_path / "summary.json"

    summary = prepare_dsbi_dataset(raw_root, output_dir, summary_path)

    cropped_files = list((output_dir / "101000").glob("*.png"))
    assert len(cropped_files) == 1
    assert summary["total_crops"] == 1

    saved_summary = json.loads(summary_path.read_text())
    assert saved_summary["class_counts"]["101000"] == 1
