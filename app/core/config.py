from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Chatbot API"
    app_env: str = "development"

    database_url: str

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:4b"
    ollama_embed_model: str = "nomic-embed-text"

    class Config:
        env_file = ".env"


settings = Settings()