from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Chatbot API"
    app_env: str = "development"

    database_url: str

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:4b"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_rewrite_enabled: bool = True
    ollama_timeout_seconds: int = 20
    ollama_rewrite_timeout_seconds: int = 8
    ollama_num_predict: int = 120
    ollama_temperature: float = 0.2
    cors_origins: list[str] = [
        "https://chatbot.gruposolar.com.br",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def ollama_base_url_normalized(self) -> str:
        return self.ollama_base_url.rstrip("/")


settings = Settings()
