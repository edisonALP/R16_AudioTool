import os
import re


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
