import numpy as np
import cv2

from braille_system.segment import detect_braille_dots, extract_candidate_cells


def test_detect_braille_dots_finds_small_dot_boxes():
    image = np.zeros((80, 80), dtype=np.uint8)
    cv2.circle(image, (20, 20), 3, 255, -1)
    cv2.circle(image, (35, 20), 3, 255, -1)

    dots = detect_braille_dots(image)

    assert len(dots) == 2
    assert dots[0][0] < dots[1][0]


def test_extract_candidate_cells_returns_sorted_boxes():
    image = np.zeros((100, 100), dtype=np.uint8)
    cv2.circle(image, (20, 20), 3, 255, -1)
    cv2.circle(image, (35, 20), 3, 255, -1)
    cv2.circle(image, (20, 35), 3, 255, -1)
    cv2.circle(image, (35, 35), 3, 255, -1)
    cv2.circle(image, (70, 20), 3, 255, -1)
    cv2.circle(image, (85, 20), 3, 255, -1)
    cv2.circle(image, (70, 35), 3, 255, -1)
    cv2.circle(image, (85, 35), 3, 255, -1)

    boxes = extract_candidate_cells(image)

    assert len(boxes) == 2
    assert boxes[0][0] < boxes[1][0]
    assert boxes[0][1] <= boxes[1][1]


def test_extract_candidate_cells_handles_slightly_uneven_spacing():
    image = np.zeros((120, 120), dtype=np.uint8)
    cv2.circle(image, (20, 20), 3, 255, -1)
    cv2.circle(image, (34, 21), 3, 255, -1)
    cv2.circle(image, (20, 38), 3, 255, -1)
    cv2.circle(image, (35, 39), 3, 255, -1)
    cv2.circle(image, (67, 20), 3, 255, -1)
    cv2.circle(image, (84, 22), 3, 255, -1)
    cv2.circle(image, (68, 39), 3, 255, -1)
    cv2.circle(image, (85, 40), 3, 255, -1)

    boxes = extract_candidate_cells(image)

    assert len(boxes) == 2
