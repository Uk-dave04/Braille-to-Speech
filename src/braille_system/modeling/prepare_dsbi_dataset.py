import json
from collections import Counter
from pathlib import Path

import cv2


def parse_dsbi_annotation(annotation_text: str) -> dict:
    lines = [line.strip() for line in annotation_text.splitlines()]
    if len(lines) < 3:
        raise ValueError("DSBI annotation must include angle, vertical lines, and horizontal lines.")

    angle = float(lines[0]) if lines[0] else 0.0
    vertical_lines = [int(value) for value in lines[1].split()] if lines[1] else []
    horizontal_lines = [int(value) for value in lines[2].split()] if lines[2] else []
    cells = []

    for raw in lines[3:]:
        if not raw:
            continue
        parts = [int(value) for value in raw.split()]
        if len(parts) != 8:
            continue
        row, col = parts[:2]
        dots = parts[2:]
        cells.append({"row": row, "col": col, "dots": dots})

    return {
        "angle": angle,
        "vertical_lines": vertical_lines,
        "horizontal_lines": horizontal_lines,
        "cells": cells,
    }


def cell_annotation_to_pattern(dots: list[int]) -> str:
    return "".join(str(int(value)) for value in dots)


def _cell_box_from_annotation(
    cell: dict,
    vertical_lines: list[int],
    horizontal_lines: list[int],
    image_width: int,
    image_height: int,
    padding: int = 4,
) -> tuple[int, int, int, int] | None:
    col_index = (cell["col"] - 1) * 2
    row_index = (cell["row"] - 1) * 3

    if col_index + 1 >= len(vertical_lines) or row_index + 2 >= len(horizontal_lines):
        return None

    x1 = max(0, vertical_lines[col_index] - padding)
    x2 = min(image_width, vertical_lines[col_index + 1] + padding)
    y1 = max(0, horizontal_lines[row_index] - padding)
    y2 = min(image_height, horizontal_lines[row_index + 2] + padding)

    if x2 <= x1 or y2 <= y1:
        return None

    return x1, y1, x2, y2


def prepare_dsbi_dataset(raw_root: Path, output_dir: Path, summary_path: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    class_counts = Counter()
    total_crops = 0

    for annotation_path in raw_root.rglob("*+recto.txt"):
        image_path = annotation_path.with_suffix(".jpg")
        if not image_path.exists():
            continue

        annotation_text = annotation_path.read_text(encoding="utf-8", errors="ignore")
        if not annotation_text.strip():
            continue

        parsed = parse_dsbi_annotation(annotation_text)
        if not parsed["cells"]:
            continue

        image = cv2.imread(str(image_path))
        if image is None:
            continue

        book_name = annotation_path.parent.name.replace(" ", "_")
        stem = image_path.stem
        height, width = image.shape[:2]

        for index, cell in enumerate(parsed["cells"]):
            box = _cell_box_from_annotation(
                cell,
                parsed["vertical_lines"],
                parsed["horizontal_lines"],
                width,
                height,
            )
            if box is None:
                continue

            x1, y1, x2, y2 = box
            crop = image[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            pattern_label = cell_annotation_to_pattern(cell["dots"])
            label_dir = output_dir / pattern_label
            label_dir.mkdir(parents=True, exist_ok=True)
            crop_path = label_dir / f"{book_name}_{stem}_{index}.png"
            cv2.imwrite(str(crop_path), crop)
            class_counts[pattern_label] += 1
            total_crops += 1

    summary = {
        "total_crops": total_crops,
        "num_classes": len(class_counts),
        "class_counts": dict(sorted(class_counts.items())),
    }
    summary_path.write_text(json.dumps(summary, indent=2))
    return summary


def main():
    project_root = Path(__file__).resolve().parents[3]
    raw_root = project_root / "data" / "raw" / "DSBI-master" / "DSBI-master" / "data"
    output_dir = project_root / "data" / "processed" / "dsbi_recto_ids"
    summary_path = project_root / "data" / "processed" / "dsbi_recto_ids_summary.json"
    summary = prepare_dsbi_dataset(raw_root, output_dir, summary_path)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
