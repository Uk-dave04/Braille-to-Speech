import numpy as np

from braille_system.inference import prepare_cell_for_model


def test_prepare_cell_for_model_returns_batched_normalized_array():
    cell = np.full((12, 8), 255, dtype=np.uint8)

    batch = prepare_cell_for_model(cell)

    assert batch.shape == (1, 32, 32, 1)
    assert batch.dtype == np.float32
    assert float(batch.min()) >= 0.0
    assert float(batch.max()) <= 1.0
