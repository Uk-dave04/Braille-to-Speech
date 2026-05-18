import numpy as np
import pytest

from braille_system.inference import predict_braille_pattern, predict_braille_patterns


class DummyModel:
    def predict(self, batch, verbose=0):
        if batch.shape == (1, 32, 32, 1):
            return np.array([[0.1, 0.8, 0.1]], dtype=np.float32)
        assert batch.shape == (2, 32, 32, 1)
        return np.array(
            [
                [0.1, 0.8, 0.1],
                [0.7, 0.2, 0.1],
            ],
            dtype=np.float32,
        )


def test_predict_braille_pattern_returns_label_and_confidence():
    model = DummyModel()
    cell = np.full((10, 10), 255, dtype=np.uint8)

    label, confidence = predict_braille_pattern(model, cell, ["100000", "110000", "100100"])

    assert label == "110000"
    assert 0.0 <= confidence <= 1.0


def test_predict_braille_patterns_returns_label_and_confidence_per_cell():
    model = DummyModel()
    cells = [
        np.full((10, 10), 255, dtype=np.uint8),
        np.zeros((12, 12), dtype=np.uint8),
    ]

    predictions = predict_braille_patterns(model, cells, ["100000", "110000", "100100"])

    assert predictions[0][0] == "110000"
    assert predictions[1][0] == "100000"
    assert predictions[0][1] == pytest.approx(0.8)
    assert predictions[1][1] == pytest.approx(0.7)


def test_predict_braille_patterns_raises_clear_error_for_label_count_mismatch():
    model = DummyModel()
    cells = [np.full((10, 10), 255, dtype=np.uint8)]

    with pytest.raises(RuntimeError, match="Label count"):
        predict_braille_patterns(model, cells, ["100000", "110000"])
