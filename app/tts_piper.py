import io
import wave


def synthesize(voice, text: str) -> bytes:
    """
    Run Piper TTS and return WAV bytes.
    """
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        voice.synthesize(text, wf)
    return buf.getvalue()
