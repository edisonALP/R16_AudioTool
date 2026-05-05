# Naming Section — Design Spec
**Date:** 2026-05-05  
**Status:** Approved

---

## Overview

Add a dedicated **Naming Section** widget to R16 AudioTool between the Drop Zone and Pattern Bar. Holds Style/Vibe Tags and multiple Producer Tags. Both feed new pattern tokens. Settings persist via `settings.json`.

Target filename format: `[analog, wavy]_beatname_130bpm_@beatsexuell_@R16Studios.mp3`

---

## Architecture

### New Files
- `src/settings.py` — read/write `settings.json` next to the executable
- `src/naming_section.py` — `NamingSection` QWidget

### Modified Files
- `src/presets.py` — new token IDs + "Loop Pool" preset
- `src/renamer.py` — new token resolution, extended `build_filename` signature
- `src/main_window.py` — insert NamingSection, wire `naming_changed` signal

### Data Flow
```
NamingSection.naming_changed(style_tags: list[str], producers: list[str])
  → MainWindow._update_all_previews()
    → _update_preview(row)
      → build_filename(..., style_tags, producers)
```

### settings.json Schema
```json
{
  "style_tags": ["analog", "wavy"],
  "custom_tags": ["mywntag"],
  "producers": ["beatsexuell", "R16Studios"]
}
```
Stored next to the app executable (or `~/.r16audiotool/settings.json` as fallback).

---

## NamingSection UI

```
▶  Naming · [analog, wavy] · @beatsexuell_@R16Studios
┌──────────────────────────────────────────────────────────┐
│  Style / Vibe Tags:                                      │
│  [analog] [wavy] [don] [ambient] [drill] [trap] ...      │
│  [● mytag ×]  [+ _____________________ ]                 │
│                                                          │
│  Producer Tags:                                          │
│  [@  beatsexuell    ]  [@  R16Studios    ]  [+]          │
└──────────────────────────────────────────────────────────┘
```

- **Toggle button** (collapsed): shows active tags + producers as inline preview
- **Style Tags row**: preset chips toggle red=active/grey=inactive; custom tags shown with `●` prefix and `×` to delete; freetext input + Enter adds custom tag
- **Producer Tags**: 1–3 text inputs; `+` button adds another (hidden when 3 already showing); `@` prefix shown as static label; placeholder text `beatsexuell` / `R16Studios` / `producer3`
- **Save**: auto-saves to `settings.json` on every change (no explicit save button needed — simpler for non-tech users)
- **Load**: on app start, load from `settings.json` and restore state

### Preset Style Tag List
`analog, don, wavy, ambient, melodic, drill, trap, afro, synth, dark, cinematic, bounce, grimey, plugg, emo, rage, jersey, uk drill, phonk`

---

## New Tokens

| Token ID | Suffix | Display Label | Example Output |
|---|---|---|---|
| `style_tags` | `""` | `[Tags]` | `[analog, wavy, don]` |
| `producers` | `""` | `@Producers` | `@beatsexuell_@R16Studios` |
| `bpm_raw` | `"bpm"` | `bpm` | `130bpm` |
| `bpm_paren` | `""` | `(BPM)` | `(130bpm)` |

Existing tokens (`name`, `key`, `bpm_raw` with `BPM`/`""`, `tag`) unchanged.

### New Preset: "Loop Pool"
```python
"Loop Pool": [("style_tags", ""), ("name", ""), ("bpm_raw", "bpm"), ("producers", "")]
# → [analog, wavy]_beatname_130bpm_@beatsexuell_@R16Studios.mp3
```

---

## renamer.py Changes

`build_filename` signature extended (backward-compatible defaults):
```python
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
```

New token resolution:
```python
if token_id == "style_tags":
    tags = [t for t in (style_tags or []) if t.strip()]
    return ("[" + ", ".join(tags) + "]") if tags else ""

if token_id == "producers":
    prods = [p.strip() for p in (producers or []) if p.strip()]
    return "_".join(f"@{p}" for p in prods) if prods else ""

if token_id == "bpm_paren":
    return f"({bpm_val}bpm)" if bpm_val else ""
```

---

## settings.py Interface

```python
def load() -> dict          # returns dict with defaults if file missing
def save(data: dict) -> None
```

Default values:
```python
DEFAULTS = {
    "style_tags": [],
    "custom_tags": [],
    "producers": ["beatsexuell"],
}
```

---

## Scope / Out of Scope

**In scope:**
- NamingSection widget with Style Tags + Producer Tags
- New tokens: `style_tags`, `producers`, `bpm_paren`, `bpm_raw+bpm`
- Loop Pool preset
- settings.json persistence

**Out of scope:**
- Per-row style tags (global only)
- Auto-genre detection (Essentia)
- GPU features
