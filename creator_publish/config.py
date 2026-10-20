"""Configuration for creator-publish: env-first, file-second.

Extracted from ShortSmash's config (2026-10-19) so multiple tools share one
publishing layer. The home directory defaults to ~/.creator-publish and can
be overridden with CREATOR_PUBLISH_HOME (ShortSmash sets it to ~/.shortsmash
so existing tokens keep working).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

HOME = Path(os.environ.get(
    "CREATOR_PUBLISH_HOME", str(Path.home() / ".creator-publish")))
CONFIG_FILE = HOME / "config.yaml"
QUEUE_DB = HOME / "queue.db"

DEFAULTS: dict[str, Any] = {
    "timezone": "America/New_York",
    "language": "en",
}


def ensure_home() -> Path:
    HOME.mkdir(parents=True, exist_ok=True)
    return HOME


def load_yaml() -> dict[str, Any]:
    if CONFIG_FILE.exists():
        try:
            import yaml
            return yaml.safe_load(CONFIG_FILE.read_text()) or {}
        except ImportError:
            return {}
    return {}


class Config:
    def __init__(self, overrides: dict[str, Any] | None = None,
                 home: Path | None = None):
        file_cfg = load_yaml()
        self._data: dict[str, Any] = {**DEFAULTS, **file_cfg, **(overrides or {})}
        self.home = home or HOME

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    # ---- secrets (env only, never written to disk by us) ----
    @staticmethod
    def secret(name: str) -> str | None:
        return os.environ.get(name) or None

    def require(self, key: str, env_name: str, what_for: str) -> str:
        val = self.secret(env_name) or self.get(key)
        if not val:
            raise RuntimeError(
                f"Missing {env_name}: needed {what_for}. "
                f"Set it in your environment or .env (see README)."
            )
        return val
