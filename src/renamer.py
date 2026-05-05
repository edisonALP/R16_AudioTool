import os
import re


_PAT_TAG = re.compile(r'@(\w+)')
_PAT_BPM = re.compile(r'\b(\d{2,3})\s*(?:BPM|bpm)\b')
_PAT_KEY = re.compile(r'\b([A-Ga-g][#b]?(?:maj|min))\b')


def parse_filename(stem: str) -> dict:
    """Extract tag, bpm, key from stem name. Returns cleaned name with tokens removed."""
    tag_m = _PAT_TAG.search(stem)
    bpm_m = _PAT_BPM.search(stem)
    key_m = _PAT_KEY.search(stem)

    tag = tag_m.group(1) if tag_m else None
    bpm = float(bpm_m.group(1)) if bpm_m else None
    key = key_m.group(1) if key_m else None

    clean = stem
    for pat in (_PAT_TAG, _PAT_BPM, _PAT_KEY):
        clean = pat.sub('', clean)
    clean = re.sub(r'[\s_\-]+', ' ', clean).strip(' _-')

    return {'tag': tag, 'bpm': bpm, 'key': key, 'clean_name': clean}


def build_filename(stem_name: str, key: str, bpm: float, tag: str, ext: str) -> str:
    bpm_str = f"{int(bpm)}BPM" if bpm == int(bpm) else f"{bpm}BPM"
    parts = [stem_name]
    if key:
        parts.append(key)
    if bpm:
        parts.append(bpm_str)
    if tag:
        parts.append(tag)
    name = '_'.join(parts)
    # sanitize
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
