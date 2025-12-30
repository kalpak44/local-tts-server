#!/usr/bin/env python3
"""
Pre-download all Silero and Piper models for offline use.
This script should be run during Docker image build.
"""
import subprocess
import pathlib
import yaml
import torch
from huggingface_hub import hf_hub_download


def download_silero_models():
    """Download all Silero models defined in voices_definitions.yaml"""
    with open("voices_definitions.yaml", "r", encoding="utf-8") as f:
        defs = yaml.safe_load(f)

    silero_def = defs["silero"]
    repo_dir = pathlib.Path(silero_def["repo_dir"])

    # Clone Silero repo
    print(f"Cloning Silero repo to {repo_dir}...")
    if not (repo_dir / "hubconf.py").exists():
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", silero_def["repo_git_url"], str(repo_dir)],
            check=True,
        )
        print("✓ Silero repo cloned")
    else:
        print("✓ Silero repo already exists")

    # Download all model files
    for model_key, model in silero_def["models"].items():
        package_url = model["package_url"]
        filename = package_url.split("/")[-1]
        model_path = repo_dir / filename

        if not model_path.exists():
            print(f"Downloading {model_key} ({filename})...")
            torch.hub.download_url_to_file(package_url, str(model_path))
            print(f"✓ {model_key} downloaded")
        else:
            print(f"✓ {model_key} already exists")


def download_piper_models():
    """Download all Piper models defined in voices_definitions.yaml"""
    with open("voices_definitions.yaml", "r", encoding="utf-8") as f:
        defs = yaml.safe_load(f)

    piper_def = defs["piper"]
    repo_id = piper_def["hf_repo_id"]

    print(f"\nDownloading Piper models from HuggingFace ({repo_id})...")

    for lang, lang_def in piper_def["languages"].items():
        for voice_id, voice in lang_def["voices"].items():
            base = voice["subpath_no_ext"]

            print(f"Downloading {voice_id} ({lang})...")

            # Download .onnx model
            onnx_path = hf_hub_download(
                repo_id=repo_id,
                filename=base + ".onnx",
            )
            print(f"  ✓ {base}.onnx")

            # Download .onnx.json config
            cfg_path = hf_hub_download(
                repo_id=repo_id,
                filename=base + ".onnx.json",
            )
            print(f"  ✓ {base}.onnx.json")


if __name__ == "__main__":
    print("=" * 60)
    print("Pre-downloading all TTS models for offline use")
    print("=" * 60)

    download_silero_models()
    download_piper_models()

    print("\n" + "=" * 60)
    print("✓ All models downloaded successfully!")
    print("=" * 60)
