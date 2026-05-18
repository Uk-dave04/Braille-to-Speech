from .decode import decode_braille_patterns


def sort_cells_into_lines(cells: list[dict], y_tolerance: int = 10) -> list[list[dict]]:
    ordered = sorted(cells, key=lambda item: (item["box"][1], item["box"][0]))
    lines: list[list[dict]] = []

    for cell in ordered:
        if not lines:
            lines.append([cell])
            continue

        current_line = lines[-1]
        previous_y = current_line[0]["box"][1]

        if abs(cell["box"][1] - previous_y) <= y_tolerance:
            current_line.append(cell)
            current_line.sort(key=lambda item: item["box"][0])
        else:
            lines.append([cell])

    return lines


def _patterns_with_inferred_spaces(line: list[dict], gap_threshold: int) -> list[str]:
    if not line:
        return []

    ordered = sorted(line, key=lambda item: item["box"][0])
    patterns: list[str] = [ordered[0]["pattern"]]

    for previous, current in zip(ordered, ordered[1:]):
        prev_x, _, prev_w, _ = previous["box"]
        curr_x, _, _, _ = current["box"]
        gap = curr_x - (prev_x + prev_w)

        if gap >= gap_threshold:
            patterns.append("SPACE")

        patterns.append(current["pattern"])

    return patterns


def reconstruct_text_lines(lines: list[list[dict]], gap_threshold: int = 24) -> str:
    decoded_lines = []
    for line in lines:
        patterns = _patterns_with_inferred_spaces(line, gap_threshold)
        decoded_lines.append(decode_braille_patterns(patterns))
    return "\n".join(decoded_lines)
