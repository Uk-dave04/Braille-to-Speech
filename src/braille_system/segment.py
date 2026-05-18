import cv2
import numpy as np


def detect_braille_dots(
    binary_image: np.ndarray,
    min_area: int = 8,
    max_area: int = 200,
) -> list[tuple[int, int, int, int]]:
    contours, _ = cv2.findContours(
        binary_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    boxes: list[tuple[int, int, int, int]] = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if min_area <= area <= max_area:
            boxes.append((x, y, w, h))

    return sorted(boxes, key=lambda item: (item[1], item[0]))


def _group_dots_into_lines(
    dot_boxes: list[tuple[int, int, int, int]],
    y_tolerance: int = 12,
) -> list[list[tuple[int, int, int, int]]]:
    lines: list[list[tuple[int, int, int, int]]] = []

    for box in sorted(dot_boxes, key=lambda item: (item[1], item[0])):
        if not lines:
            lines.append([box])
            continue

        current_line = lines[-1]
        reference_y = current_line[0][1]
        if abs(box[1] - reference_y) <= y_tolerance:
            current_line.append(box)
        else:
            lines.append([box])

    return lines


def _estimate_spacing(dot_boxes: list[tuple[int, int, int, int]]) -> tuple[int, int]:
    if len(dot_boxes) < 2:
        return 22, 24

    xs = sorted(box[0] for box in dot_boxes)
    ys = sorted(box[1] for box in dot_boxes)

    x_diffs = [b - a for a, b in zip(xs, xs[1:]) if 0 < (b - a) <= 40]
    y_diffs = [b - a for a, b in zip(ys, ys[1:]) if 0 < (b - a) <= 40]

    x_gap = int(np.median(x_diffs)) if x_diffs else 22
    y_gap = int(np.median(y_diffs)) if y_diffs else 24

    return max(14, x_gap + 6), max(16, y_gap + 8)


def _merge_dot_line_into_cells(
    line: list[tuple[int, int, int, int]],
    x_gap_tolerance: int = 22,
    padding: int = 4,
) -> list[tuple[int, int, int, int]]:
    if not line:
        return []

    ordered = sorted(line, key=lambda item: item[0])
    groups: list[list[tuple[int, int, int, int]]] = [[ordered[0]]]

    for box in ordered[1:]:
        prev = groups[-1][-1]
        prev_right = prev[0] + prev[2]
        gap = box[0] - prev_right
        if gap <= x_gap_tolerance:
            groups[-1].append(box)
        else:
            groups.append([box])

    merged: list[tuple[int, int, int, int]] = []
    for group in groups:
        xs = [box[0] for box in group]
        ys = [box[1] for box in group]
        rights = [box[0] + box[2] for box in group]
        bottoms = [box[1] + box[3] for box in group]
        x = max(0, min(xs) - padding)
        y = max(0, min(ys) - padding)
        w = max(rights) - min(xs) + (padding * 2)
        h = max(bottoms) - min(ys) + (padding * 2)
        merged.append((x, y, w, h))

    return merged


def _merge_cells_vertically(
    boxes: list[tuple[int, int, int, int]],
    x_tolerance: int = 12,
    y_gap_tolerance: int = 24,
) -> list[tuple[int, int, int, int]]:
    if not boxes:
        return []

    ordered = sorted(boxes, key=lambda item: (item[0], item[1]))
    merged: list[tuple[int, int, int, int]] = []
    used = [False] * len(ordered)

    for idx, box in enumerate(ordered):
        if used[idx]:
            continue

        x, y, w, h = box
        current = [x, y, x + w, y + h]
        used[idx] = True

        for other_idx in range(idx + 1, len(ordered)):
            if used[other_idx]:
                continue

            ox, oy, ow, oh = ordered[other_idx]
            same_column = abs(ox - x) <= x_tolerance and abs((ox + ow) - (x + w)) <= x_tolerance
            vertical_gap = oy - current[3]
            if same_column and vertical_gap <= y_gap_tolerance:
                current[0] = min(current[0], ox)
                current[1] = min(current[1], oy)
                current[2] = max(current[2], ox + ow)
                current[3] = max(current[3], oy + oh)
                used[other_idx] = True

        merged.append((current[0], current[1], current[2] - current[0], current[3] - current[1]))

    return sorted(merged, key=lambda item: (item[1], item[0]))


def extract_candidate_cells(
    binary_image: np.ndarray,
    min_area: int = 8,
) -> list[tuple[int, int, int, int]]:
    dot_boxes = detect_braille_dots(binary_image, min_area=min_area)
    x_gap_tolerance, y_gap_tolerance = _estimate_spacing(dot_boxes)
    lines = _group_dots_into_lines(dot_boxes)

    cell_boxes: list[tuple[int, int, int, int]] = []
    for line in lines:
        cell_boxes.extend(_merge_dot_line_into_cells(line, x_gap_tolerance=x_gap_tolerance))

    return _merge_cells_vertically(cell_boxes, y_gap_tolerance=y_gap_tolerance)
