import yaml
import torch
from huggingface_hub import hf_hub_download
from piper.voice import PiperVoice

from app.config import settings
from app.models import voices, silero_models, piper_models
from app.silero_setup import ensure_silero_repo, ensure_silero_model


def load_all():
    """
    Load models and register voices at startup.
    """
    with open("voices_definitions.yaml", "r", encoding="utf-8") as f:
        defs = yaml.safe_load(f)

    # -------- Silero --------
    if "silero" in settings.engines:
        silero_def = defs["silero"]

        ensure_silero_repo(
            silero_def["repo_dir"],
            silero_def["repo_git_url"],
        )

        for model_key, model in silero_def["models"].items():
            lang = model["language_code"]
            if lang not in settings.languages:
                continue

            ensure_silero_model(
                silero_def["repo_dir"],
                model["package_url"],
            )

            loaded = torch.hub.load(
                repo_or_dir=silero_def["repo_dir"],
                model="silero_tts",
                language=lang,
                speaker=model["model_id"],
                source="local",
                trust_repo=True,
            )[0]

            silero_models[model_key] = loaded

            for vid, name in model.get("voices", {}).items():
                voices[vid] = {
                    "name": name,
                    "engine": "silero",
                    "model": model_key,
                    "sr": 48000,
                }

    # -------- Piper --------
    if "piper" in settings.engines:
        for lang, lang_def in defs["piper"]["languages"].items():
            if lang not in settings.languages:
                continue

            for vid, v in lang_def["voices"].items():
                base = v["subpath_no_ext"]

                onnx = hf_hub_download(
                    repo_id=defs["piper"]["hf_repo_id"],
                    filename=base + ".onnx",
                )
                cfg = hf_hub_download(
                    repo_id=defs["piper"]["hf_repo_id"],
                    filename=base + ".onnx.json",
                )

                piper_models[vid] = PiperVoice.load(onnx, cfg)

                voices[vid] = {
                    "name": v["name"],
                    "engine": "piper",
                }
