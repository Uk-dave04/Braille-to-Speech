from braille_system.utils import normalize_text_for_tts


def test_normalize_text_for_tts_collapses_whitespace():
    assert normalize_text_for_tts("hello   world\n\nagain") == "hello world again"


def test_normalize_text_for_tts_preserves_basic_punctuation_spacing():
    assert normalize_text_for_tts("hello , world .") == "hello, world."
