import numpy as np

from braille_system.modeling.train import split_train_validation


def test_split_train_validation_handles_singleton_classes():
    x = np.arange(60).reshape(10, 3, 2, 1)
    y = np.array(
        [
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        dtype=np.float32,
    )
    y[7, 3] = 1

    x_train, x_val, y_train, y_val = split_train_validation(x, y, test_size=0.2, random_state=42)

    assert len(x_train) + len(x_val) == len(x)
    assert len(y_train) + len(y_val) == len(y)
