from braille_system.reconstruct import reconstruct_text_lines, sort_cells_into_lines


def test_sort_cells_groups_rows_by_y_coordinate():
    cells = [
        {"box": (10, 12, 18, 30), "pattern": "100000"},
        {"box": (40, 11, 18, 30), "pattern": "110000"},
        {"box": (12, 60, 18, 30), "pattern": "100100"},
    ]

    lines = sort_cells_into_lines(cells, y_tolerance=12)

    assert len(lines) == 2
    assert [cell["pattern"] for cell in lines[0]] == ["100000", "110000"]
    assert [cell["pattern"] for cell in lines[1]] == ["100100"]


def test_reconstruct_text_lines_joins_patterns_into_sentence():
    lines = [
        [
            {"box": (10, 10, 18, 30), "pattern": "100000"},
            {"box": (35, 10, 18, 30), "pattern": "110000"},
        ],
        [
            {"box": (10, 50, 18, 30), "pattern": "100100"},
        ],
    ]

    assert reconstruct_text_lines(lines) == "ab\nc"


def test_reconstruct_text_lines_infers_space_from_large_gap():
    lines = [
        [
            {"box": (10, 10, 18, 30), "pattern": "100000"},
            {"box": (70, 10, 18, 30), "pattern": "110000"},
        ],
    ]

    assert reconstruct_text_lines(lines, gap_threshold=30) == "a b"
