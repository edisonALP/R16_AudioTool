PRESETS: dict[str, list[tuple[str, str]]] = {
    "Splice":    [("tag", ""), ("name", ""), ("bpm_raw", ""), ("key", "")],
    "Looperman": [("name", ""), ("bpm_raw", "bpm"), ("key", "")],
    "Classic":   [("name", ""), ("key", ""), ("bpm_raw", "BPM"), ("tag", "")],
    "Minimal":   [("name", ""), ("key", ""), ("bpm_raw", "")],
    "Custom":    [],
}

AVAILABLE_TOKENS: list[tuple[str, str, str]] = [
    # (token_id, suffix, display_label)
    ("name",    "",    "Name"),
    ("key",     "",    "Key"),
    ("bpm_raw", "BPM", "BPM"),
    ("bpm_raw", "",    "BPM#"),
    ("tag",     "",    "Tag"),
]
