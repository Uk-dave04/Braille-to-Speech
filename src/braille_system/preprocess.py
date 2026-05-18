import cv2
import numpy as np


def crop_page_region(image: np.ndarray, min_area_ratio: float = 0.2) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return image

    image_area = image.shape[0] * image.shape[1]
    candidate = max(contours, key=cv2.contourArea)
    if cv2.contourArea(candidate) < image_area * min_area_ratio:
        return image

    x, y, w, h = cv2.boundingRect(candidate)
    return image[y:y + h, x:x + w]


def preprocess_braille_image(image: np.ndarray) -> np.ndarray:
    page = crop_page_region(image)
    gray = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    normalized = cv2.normalize(blur, None, 0, 255, cv2.NORM_MINMAX)
    normalized = cv2.equalizeHist(normalized)
    binary = cv2.adaptiveThreshold(
        normalized,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        6,
    )
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return cleaned
