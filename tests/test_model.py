from braille_system.modeling.model import build_braille_cnn


def test_build_braille_cnn_output_classes():
    model = build_braille_cnn((32, 32, 1), 64)
    assert model.output_shape == (None, 64)
