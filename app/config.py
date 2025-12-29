from dotenv import dotenv_values


class Settings:
    """
    Application configuration loaded from config.env
    """

    def __init__(self):
        env = dotenv_values("config.env")

        self.languages = set(filter(None, (env.get("LANGUAGES") or "").split(",")))
        self.engines = set(filter(None, (env.get("ENABLED_ENGINES") or "").split(",")))

        self.default_voice = env.get("DEFAULT_VOICE", "")
        self.silero_quality = env.get("SILERO_QUALITY", "high")

        self.device = env.get("DEVICE", "cpu")
        self.cpu_threads = int(env.get("TORCH_CPU_THREADS", "0"))


settings = Settings()
