from fastapi import FastAPI
from app.api import router
from app.loader import load_all

app = FastAPI(title="Local TTS")

@app.on_event("startup")
def startup():
    load_all()

app.include_router(router)
