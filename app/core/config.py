from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # NVIDIA Configuration
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_speech_model: str = "nvidia/parakeet-rnnt-1.1b"
    nvidia_llm_model: str = "meta/llama-3.1-70b-instruct"
    nvidia_timeout: float = 30.0

    # Application Configuration
    echoflow_hotkey: str = "ctrl+space"
    echoflow_auto_start: bool = False
    echoflow_log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
