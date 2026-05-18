import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
RUNTIME_DIR = Path(tempfile.gettempdir()) / "braille_to_speech_runtime"
UPLOAD_DIR = RUNTIME_DIR / "uploads"
AUDIO_DIR = RUNTIME_DIR / "audio"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "braille_cnn.keras"
PROCESSED_DATASET_DIR = BASE_DIR / "data" / "processed" / "braille_segment_character_natural_ids"
