import json
import os
import warnings

_DEFAULTS: dict = {
    "style_tags": [],
    "custom_tags": [],
    "producers": ["beatsexuell"],
    "gpu_mode": "auto",
    "gpu_setup_done": False,
}


def _path() -> str:
    if os.name == "nt":
        base = os.path.join(
            os.environ.get("APPDATA", os.path.expanduser("~")), "R16AudioTool"
        )
    else:
        # macOS: ~/Library/Application Support/R16AudioTool
        base = os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", "R16AudioTool"
        )
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "settings.json")


def load() -> dict:
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
        return {**_DEFAULTS, **data}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULTS)


def save(data: dict) -> None:
    try:
        path = _path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        warnings.warn(f"Settings could not be saved: {exc}")
