from braille_system.decode import decode_braille_patterns


def test_decode_simple_letters():
    patterns = ["100000", "110000", "100100"]
    assert decode_braille_patterns(patterns) == "abc"


def test_decode_number_sequence():
    patterns = ["001111", "100000", "110000", "100100"]
    assert decode_braille_patterns(patterns) == "123"


def test_decode_space_token():
    patterns = ["100000", "SPACE", "110000"]
    assert decode_braille_patterns(patterns) == "a b"


def test_decode_unknown_pattern_falls_back_to_question_mark():
    patterns = ["111111"]
    assert decode_braille_patterns(patterns) == "?"


def test_decode_basic_punctuation():
    patterns = ["100000", "010011", "110000"]
    assert decode_braille_patterns(patterns) == "a.b"
