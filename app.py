import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from config import AUDIO_DIR, BASE_DIR, UPLOAD_DIR
from src.braille_system.gemini_fallback import GeminiRecognitionError, correct_recognized_text, recognize_braille_with_gemini
from src.braille_system.io import ensure_runtime_dirs
from src.braille_system.tts import SpitchSynthesisError, build_audio_output_path, synthesize_text_to_speech
from src.braille_system.translation import GeminiTranslationError, translate_english_to_yoruba
from src.braille_system.utils import normalize_text_for_tts

app = Flask(__name__)
ensure_runtime_dirs(Path(__file__).resolve().parent)
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


def _build_processing_error_message(exc: Exception, stage: str) -> str:
    message = str(exc)
    upper_message = message.upper()
    if "503" in upper_message and "UNAVAILABLE" in upper_message:
        return (
            f"The {stage} service is temporarily busy. "
            "Please wait a moment and try again."
        )
    return message


@app.route("/")
def index():
    return render_template("index.html", error_message=None)


@app.route("/predict", methods=["POST"])
def predict():
    uploaded = request.files.get("image")
    if uploaded is None or uploaded.filename == "":
        return render_template("index.html", error_message="Image upload is required."), 400

    filename = secure_filename(uploaded.filename)
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        return render_template("index.html", error_message="Unsupported file type. Please upload a PNG, JPG, BMP, or WebP image."), 400

    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    try:
        uploaded_path = UPLOAD_DIR / unique_filename
        uploaded.save(uploaded_path)
    except Exception as exc:
        return render_template("index.html", error_message=f"Unable to store the uploaded image: {exc}"), 502

    try:
        raw_text = recognize_braille_with_gemini(uploaded_path)
        english_text = normalize_text_for_tts(correct_recognized_text(raw_text))
    except Exception as exc:
        return render_template(
            "index.html",
            error_message=_build_processing_error_message(exc, "recognition"),
        ), 502

    try:
        translation = translate_english_to_yoruba(english_text)
    except Exception as exc:
        return render_template(
            "index.html",
            error_message=_build_processing_error_message(exc, "translation"),
        ), 502

    speech_text = translation.translated_text
    speech_language = "yo"
    audio_path = build_audio_output_path(AUDIO_DIR, uuid.uuid4().hex)

    try:
        synthesize_text_to_speech(speech_text, audio_path, lang=speech_language)
    except Exception as exc:
        return render_template("index.html", error_message=str(exc)), 502

    return render_template(
        "result.html",
        recognized_text=english_text,
        translated_text=translation.translated_text,
        translation_used=translation.used_translation,
        translation_error=translation.fallback_reason,
        speech_language=speech_language,
        audio_file=audio_path.name,
    )


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/audio/<path:filename>")
def audio_file(filename: str):
    target = AUDIO_DIR / filename
    if not target.exists():
        abort(404)
    return send_from_directory(AUDIO_DIR, filename)


@app.route("/debug/<path:filepath>")
def debug_file(filepath: str):
    debug_root = BASE_DIR / "debug"
    target = debug_root / filepath
    if not target.exists():
        abort(404)
    return send_from_directory(debug_root, filepath)


if __name__ == "__main__":
    app.run(debug=True)
