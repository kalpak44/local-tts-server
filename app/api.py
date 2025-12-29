from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import wave
import io

from app.models import voices, silero_models, piper_models
from app.tts_silero import synthesize as silero_tts
from app.tts_piper import synthesize as piper_tts

router = APIRouter()


@router.get("/audio/voices")
def list_voices():
    return {
        "voices": [
            {"id": vid, "name": meta["name"]}
            for vid, meta in voices.items()
        ]
    }


@router.post("/audio/speech")
def speech(payload: dict):
    text = payload.get("input")
    voice_id = payload.get("voice")

    if not text:
        raise HTTPException(400, "Missing input text")

    if voice_id not in voices:
        raise HTTPException(400, "Invalid voice id")

    meta = voices[voice_id]

    if meta["engine"] == "silero":
        model = silero_models[meta["model"]]
        pcm = silero_tts(model, text, voice_id, meta["sr"])

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(meta["sr"])
            wf.writeframes(pcm)

        return Response(buf.getvalue(), media_type="audio/wav")

    audio = piper_tts(piper_models[voice_id], text)
    return Response(audio, media_type="audio/wav")
