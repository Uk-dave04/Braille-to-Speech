from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path

import cv2

from config import BASE_DIR, MODEL_PATH
from .inference import load_inference_model, predict_braille_patterns
from .modeling.train import resolve_dataset_roots
from .preprocess import preprocess_braille_image
from .reconstruct import reconstruct_text_lines, sort_cells_into_lines
from .segment import extract_candidate_cells

_MODEL_CACHE: dict[Path, object] = {}


@dataclass
class RecognitionResult:
    text: str
    confidences: list[float] = field(default_factory=list)
    cells_detected: int = 0
    debug_artifacts: dict[str, Path] = field(default_factory=dict)
    model_used: bool = False


def _discover_class_names(dataset_dir: Path | list[Path] | None = None) -> list[str]:
    roots = resolve_dataset_roots(dataset_dir)
    class_names: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        class_names.update(path.name for path in root.iterdir() if path.is_dir())
    return sorted(class_names)


def _load_model_class_names(model_path: Path) -> list[str]:
    labels_path = model_path.with_suffix(".labels.json")
    if not labels_path.exists():
        return []

    loaded = json.loads(labels_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, list) or not all(isinstance(item, str) for item in loaded):
        raise RuntimeError(f"Invalid model label file: {labels_path}")
    return loaded


def _build_overlay_image(image, boxes: list[tuple[int, int, int, int]]):
    overlay = image.copy()
    for x, y, w, h in boxes:
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return overlay


def _save_debug_artifacts(
    image_path: Path,
    image,
    binary,
    boxes: list[tuple[int, int, int, int]],
    debug_root: Path,
) -> dict[str, Path]:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run_dir = debug_root / f"{image_path.stem}-{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    original_path = run_dir / "original.png"
    binary_path = run_dir / "binary.png"
    overlay_path = run_dir / "overlay.png"

    cv2.imwrite(str(original_path), image)
    cv2.imwrite(str(binary_path), binary)
    cv2.imwrite(str(overlay_path), _build_overlay_image(image, boxes))

    return {
        "original": original_path,
        "binary": binary_path,
        "overlay": overlay_path,
    }


def clear_model_cache() -> None:
    _MODEL_CACHE.clear()


def _get_cached_model(model_path: Path):
    resolved = model_path.resolve()
    model = _MODEL_CACHE.get(resolved)
    if model is None:
        model = load_inference_model(resolved)
        _MODEL_CACHE[resolved] = model
    return model


def process_uploaded_braille_image(
    image_path: Path,
    model_path: Path | None = None,
    dataset_dir: Path | list[Path] | None = None,
    debug_root: Path | None = None,
    save_debug_artifacts: bool = False,
) -> RecognitionResult:
    model_path = model_path or MODEL_PATH
    dataset_dir = resolve_dataset_roots(dataset_dir)
    debug_root = debug_root or (BASE_DIR / "debug")

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read uploaded image: {image_path}")

    binary = preprocess_braille_image(image)
    boxes = extract_candidate_cells(binary)
    debug_artifacts = (
        _save_debug_artifacts(image_path, image, binary, boxes, debug_root)
        if save_debug_artifacts
        else {}
    )

    class_names = _load_model_class_names(model_path) or _discover_class_names(dataset_dir)
    if not model_path.exists() or not class_names:
        return RecognitionResult(
            text="demo output",
            confidences=[],
            cells_detected=len(boxes),
            debug_artifacts=debug_artifacts,
            model_used=False,
        )

    model = _get_cached_model(model_path)
    cells = []
    crops = [binary[y:y + h, x:x + w] for x, y, w, h in boxes]
    predictions = predict_braille_patterns(model, crops, class_names)
    confidences: list[float] = []

    for (x, y, w, h), (pattern, confidence) in zip(boxes, predictions):
        cells.append({"box": (x, y, w, h), "pattern": pattern, "confidence": confidence})
        confidences.append(confidence)

    lines = sort_cells_into_lines(cells)
    text = reconstruct_text_lines(lines) if lines else ""
    return RecognitionResult(
        text=text,
        confidences=confidences,
        cells_detected=len(cells),
        debug_artifacts=debug_artifacts,
        model_used=True,
    )
