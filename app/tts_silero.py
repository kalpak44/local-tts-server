import numpy as np


def synthesize(model, text: str, speaker: str, sample_rate: int) -> bytes:
    """
    Run Silero TTS and return WAV PCM bytes.
    """
    audio = model.apply_tts(
        text=text,
        speaker=speaker,
        sample_rate=sample_rate,
    )

    audio = audio.cpu().numpy()

    peak = max(1e-4, abs(audio).max())
    audio = (audio / peak * 32767).astype(np.int16)

    return audio.tobytes()
