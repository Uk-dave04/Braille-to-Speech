from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

from config import MODEL_PATH
from .train import load_dataset, resolve_dataset_roots


def main():
    try:
        from tensorflow import keras
    except ImportError as exc:
        raise RuntimeError(
            "TensorFlow is required to evaluate the Braille CNN."
        ) from exc

    model = keras.models.load_model(MODEL_PATH)
    x, y, label_names = load_dataset(resolve_dataset_roots())
    predictions = model.predict(x).argmax(axis=1)
    truth = y.argmax(axis=1)

    print(classification_report(truth, predictions, target_names=label_names, zero_division=0))

    matrix = confusion_matrix(truth, predictions)
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, cmap="Blues")
    plt.title("Braille Cell Confusion Matrix")
    plt.tight_layout()
    Path("outputs").mkdir(exist_ok=True)
    plt.savefig("outputs/confusion_matrix.png")


if __name__ == "__main__":
    main()
