import re


def normalize_text_for_tts(text: str) -> str:
    normalized = " ".join(text.split())
    normalized = re.sub(r"\s+([,.;:!?])", r"\1", normalized)
    normalized = normalized.strip("\"'` ")
    return normalized.strip()
