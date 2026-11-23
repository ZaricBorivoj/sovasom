import os
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


def database_secret() -> str:
    if path := os.environ.get("DATABASE_URL_FILE"):
        return Path(path).read_text().strip()
    raise ValueError("Set DATABASE_URL or DATABASE_URL_FILE")


class Settings(BaseSettings):
    database_url: str = Field(default_factory=database_secret, repr=False)
    public_origin: str = "https://testserver"

    @field_validator("public_origin")
    @classmethod
    def https_origin(cls, value: str) -> str:
        parsed = urlsplit(value)
        if parsed.scheme != "https" or not parsed.netloc or parsed.path:
            raise ValueError("PUBLIC_ORIGIN must be an HTTPS origin without a path")
        return value
