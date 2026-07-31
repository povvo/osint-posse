"""Config management — ~/.config/ospo/config.toml"""

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]


import tomli_w

from ._paths import CONFIG_DIR, CONFIG_FILE

DEFAULTS: dict = {
    "model": "claude-sonnet-4-5",
    "installed_claude_agents": False,
    "installed_codex_agents": False,
}


def load() -> dict:
    if not CONFIG_FILE.exists():
        return DEFAULTS.copy()
    with CONFIG_FILE.open("rb") as f:
        return {**DEFAULTS, **tomllib.load(f)}


def save(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("wb") as f:
        tomli_w.dump(cfg, f)


def get(key: str):
    return load().get(key, DEFAULTS.get(key))


def set(key: str, value) -> None:
    cfg = load()
    cfg[key] = value
    save(cfg)
