from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
UPLOAD_DIR = BASE_DIR / "uploads"
AUDIO_DIR = BASE_DIR / "outputs" / "audio"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "braille_cnn.keras"
PROCESSED_DATASET_DIR = BASE_DIR / "data" / "processed" / "braille_segment_character_natural_ids"
