import os
import re


_PAT_TAG = re.compile(r'@(\w+?)(?=[\s@]|$)')
_PAT_BPM = re.compile(r'(?<![a-zA-Z\d])(\d{2,3})\s*(?:BPM|bpm)(?![a-zA-Z\d])')
_PAT_KEY = re.compile(r'\b([A-Ga-g][#b]?(?:maj|min))(?=[\s_\-.]|$)')


def parse_filename(stem: str) -> dict:
    """Extract tag, bpm, key from stem name. Returns cleaned name with tokens removed."""
    tag_m = _PAT_TAG.search(stem)
    bpm_m = _PAT_BPM.search(stem)
    key_m = _PAT_KEY.search(stem)

    tag = tag_m.group(1) if tag_m else None
    bpm = float(bpm_m.group(1)) if bpm_m else None
    key = key_m.group(1) if key_m else None

    # Normalize key to title case (e.g. D#min, Gmaj)
    if key:
        key = key[0].upper() + key[1:]

    clean = stem
    for pat in (_PAT_TAG, _PAT_BPM, _PAT_KEY):
        clean = pat.sub('', clean)
    clean = re.sub(r'[\s_\-]+', ' ', clean).strip(' _-')

    return {'tag': tag, 'bpm': bpm, 'key': key, 'clean_name': clean}


def build_filename(
    clean_name: str,
    key: str,
    bpm: float,
    tag: str,
    ext: str,
    pattern: list[tuple[str, str]],
    style_tags: list[str] | None = None,
    producers: list[str] | None = None,
) -> str:
    bpm_val = int(bpm) if bpm and bpm == int(bpm) else bpm

    def resolve(token_id: str, suffix: str) -> str:
        if token_id == "name":
            return clean_name or ""
        if token_id == "key":
            return (key + suffix) if key else ""
        if token_id in ("bpm", "bpm_raw"):
            return (str(bpm_val) + suffix) if bpm_val else ""
        if token_id == "bpm_paren":
            return f"({bpm_val}bpm)" if bpm_val else ""
        if token_id == "tag":
            return (tag + suffix) if tag else ""
        if token_id == "style_tags":
            tags = [t.strip() for t in (style_tags or []) if t.strip()]
            return ("[" + ", ".join(tags) + "]") if tags else ""
        if token_id == "producers":
            prods = [p.strip() for p in (producers or []) if p.strip()]
            return "_".join(f"@{p}" for p in prods) if prods else ""
        return ""

    parts = [resolve(tid, sfx) for tid, sfx in pattern]
    parts = [p for p in parts if p]
    name = "_".join(parts)
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name + ext


def rename_file(old_path: str, new_name: str) -> str:
    directory = os.path.dirname(old_path)
    new_path = os.path.join(directory, new_name)

    # avoid overwrite
    if os.path.exists(new_path) and old_path != new_path:
        base, ext = os.path.splitext(new_name)
        counter = 1
        while os.path.exists(os.path.join(directory, f"{base}_{counter}{ext}")):
            counter += 1
        new_path = os.path.join(directory, f"{base}_{counter}{ext}")

    os.rename(old_path, new_path)
    return new_path
