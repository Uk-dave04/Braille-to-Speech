import numpy as np

from braille_system.modeling.train import compute_class_weights


def test_compute_class_weights_gives_higher_weight_to_rare_classes():
    y = np.array(
        [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        dtype=np.float32,
    )

    weights = compute_class_weights(y)

    assert weights[1] > weights[0]
    assert weights[2] > weights[0]
