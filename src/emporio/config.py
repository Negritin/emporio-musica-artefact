"""Configuração de ambiente: os segredos nunca entram nas respostas."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    api_key: str = field(repr=False, default="")
    database_url: str = field(repr=False, default="")
    model: str = "openai/gpt-4.1-mini"
    embedding_model: str = "openai/text-embedding-3-small"
    embedding_dimensions: int = 1536
    max_tokens: int = 1000
    max_message_chars: int = 2000
    history_turns: int = 4
    timeout_seconds: int = 40
    max_session_turns: int = 30

    @classmethod
    def load(cls, *, admin: bool = False) -> "Settings":
        load_dotenv(ROOT / ".env.local", override=False)
        return cls(
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            database_url=os.getenv("SUPABASE_DB_URL" if admin else "ARTEFACT_APP_DB_URL", ""),
            model=os.getenv("OPENROUTER_MODEL") or "openai/gpt-4.1-mini",
            embedding_model=os.getenv("OPENROUTER_EMBEDDING_MODEL")
            or "openai/text-embedding-3-small",
            max_tokens=int(os.getenv("MAX_RESPONSE_TOKENS", "1000")),
            max_session_turns=int(os.getenv("MAX_SESSION_TURNS", "30")),
        )

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("Configure OPENROUTER_API_KEY no .env.local.")
        if not self.database_url:
            raise ValueError("Configure a conexão do banco antes de executar; veja o README.")
