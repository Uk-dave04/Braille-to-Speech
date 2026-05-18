def build_braille_cnn(input_shape: tuple[int, int, int], num_classes: int):
    try:
        from tensorflow import keras
    except ImportError as exc:
        raise RuntimeError(
            "TensorFlow is required to build the Braille CNN. "
            "Install it in the project virtual environment before training."
        ) from exc

    model = keras.Sequential(
        [
            keras.layers.Input(shape=input_shape),
            keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model
