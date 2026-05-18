import json
from collections import Counter
from pathlib import Path

import cv2


def parse_annotation_line(annotation_line: str) -> dict:
    parts = annotation_line.strip().rstrip(",").split(",")
    coords = [int(float(value)) for value in parts[:-1]]
    xs = coords[0::2]
    ys = coords[1::2]
    return {
        "bbox": (min(xs), min(ys), max(xs), max(ys)),
        "label": parts[-1],
    }


def decimal_label_to_pattern(label: str) -> str:
    value = int(label)
    return "".join("1" if value & weight else "0" for weight in (1, 2, 4, 8, 16, 32))


def prepare_character_dataset(raw_root: Path, output_dir: Path, summary_path: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    class_counts = Counter()
    total_crops = 0

    for annotation_path in raw_root.rglob("*.txt"):
        image_path = annotation_path.with_suffix(".jpg")
        if not image_path.exists():
            continue

        image = cv2.imread(str(image_path))
        if image is None:
            continue

        stem = image_path.stem
        subset = annotation_path.parent.name

        for index, line in enumerate(annotation_path.read_text().splitlines()):
            line = line.strip()
            if not line:
                continue

            parsed = parse_annotation_line(line)
            x1, y1, x2, y2 = parsed["bbox"]
            crop = image[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            pattern_label = decimal_label_to_pattern(parsed["label"])
            label_dir = output_dir / pattern_label
            label_dir.mkdir(parents=True, exist_ok=True)
            crop_path = label_dir / f"{subset}_{stem}_{index}.png"
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
    raw_root = project_root / "data" / "raw" / "braille_segment_character_natural" / "braille_segment_character_natural" / "character_label" / "icdar-2015-data"
    output_dir = project_root / "data" / "processed" / "braille_segment_character_natural_ids"
    summary_path = project_root / "data" / "processed" / "braille_segment_character_natural_ids_summary.json"
    summary = prepare_character_dataset(raw_root, output_dir, summary_path)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
