"""Configuration read from environment variables (or a local .env file).

Each field maps to the upper-case variable of the same name, e.g.
`storage_backend` <- STORAGE_BACKEND. Nothing secret is ever hard-coded here.
"""

from pathlib import Path
from typing import Literal, Self

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",  # optional: only read if present in the working directory
        extra="ignore",  # .env also holds variables for other services (Postgres, nginx...)
    )

    # "local" = files under local_data_dir (dev, CI); "r2" = Cloudflare R2 (prod).
    storage_backend: Literal["local", "r2"] = "local"
    local_data_dir: Path = Path("data")

    # Only required when storage_backend == "r2".
    r2_account_id: str | None = None
    r2_access_key_id: str | None = None
    # SecretStr hides the value in repr() and logs; call .get_secret_value() to read it.
    r2_secret_access_key: SecretStr | None = None
    r2_bucket: str | None = None

    @model_validator(mode="after")
    def _require_r2_credentials(self) -> Self:
        """Fail at startup, not at the first upload, if R2 is selected but incomplete."""
        if self.storage_backend == "r2":
            required = ("r2_account_id", "r2_access_key_id", "r2_secret_access_key", "r2_bucket")
            missing = [name.upper() for name in required if not getattr(self, name)]
            if missing:
                raise ValueError(f"STORAGE_BACKEND=r2 requires: {', '.join(missing)}")
        return self
