PRESETS: dict[str, list[tuple[str, str]]] = {
    "Splice":    [("tag", ""), ("name", ""), ("bpm_raw", ""), ("key", "")],
    "Looperman": [("name", ""), ("bpm_raw", "bpm"), ("key", "")],
    "Classic":   [("name", ""), ("key", ""), ("bpm_raw", "BPM"), ("tag", "")],
    "Minimal":   [("name", ""), ("key", ""), ("bpm_raw", "")],
    "Loop Pool": [("style_tags", ""), ("name", ""), ("bpm_raw", "bpm"), ("producers", "")],
    "Custom":    [],
}

AVAILABLE_TOKENS: list[tuple[str, str, str]] = [
    # (token_id, suffix, display_label)
    ("name",       "",     "Name"),
    ("key",        "",     "Key"),
    ("bpm_raw",    "BPM",  "BPM"),
    ("bpm_raw",    "",     "BPM#"),
    ("bpm_raw",    "bpm",  "bpm"),
    ("bpm_paren",  "",     "(BPM)"),
    ("tag",        "",     "Tag"),
    ("style_tags", "",     "[Tags]"),
    ("producers",  "",     "@Producers"),
]
