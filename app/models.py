"""
Central in-memory registries for loaded models and voices.
"""

# silero model_key -> torch model
silero_models = {}

# piper voice_id -> PiperVoice
piper_models = {}

# voice_id -> metadata
voices = {}
