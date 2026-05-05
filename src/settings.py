import json
import os

_DEFAULTS: dict = {
    "style_tags": [],
    "custom_tags": [],
    "producers": ["beatsexuell"],
}


def _path() -> str:
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(app_root, "settings.json")


def load() -> dict:
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
        return {**_DEFAULTS, **data}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULTS)


def save(data: dict) -> None:
    with open(_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
