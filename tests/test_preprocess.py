import numpy as np
import cv2

from braille_system.preprocess import preprocess_braille_image


def test_preprocess_returns_binary_image():
    image = np.full((80, 80, 3), 255, dtype=np.uint8)
    result = preprocess_braille_image(image)

    assert result.ndim == 2
    assert result.shape == (80, 80)
    assert set(np.unique(result)).issubset({0, 255})


def test_preprocess_crops_main_page_region_and_preserves_inner_signal():
    image = np.zeros((120, 120, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (100, 100), (245, 245, 245), -1)
    cv2.circle(image, (55, 55), 4, (180, 180, 180), -1)

    result = preprocess_braille_image(image)

    assert result.ndim == 2
    assert result.shape[0] < 120
    assert result.shape[1] < 120
    assert set(np.unique(result)).issubset({0, 255})
