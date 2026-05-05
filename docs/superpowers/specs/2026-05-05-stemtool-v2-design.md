# BZS Stem Tool v2 — Design Spec
**Date:** 2026-05-05  
**Author:** R16 / Edison ALP

---

## Overview

Extends the existing BZS Stem Tool with four major feature areas:

1. **Smart Name Parser** — detect Key/BPM/Tag in existing filenames, replace instead of duplicate
2. **Extended Analyzer** — Camelot notation, confidence score, stem-type classification, beat description
3. **Metadata Writer** — write ID3/FLAC/WAV tags after rename
4. **Folder Export** — organized multi-file export with user-selected structure

Bonus features included: Camelot column, confidence column (color-coded).

---

## Architecture

### New / Modified Files

```
src/
  renamer.py      ← add parse_filename()
  analyzer.py     ← extend analyze_file(): camelot, confidence, stem_type, description
  metadata.py     ← NEW: mutagen-based tag writer
  exporter.py     ← NEW: folder export logic
  main_window.py  ← UI: checkbox, new columns, export button/dialog
```

### Data Flow

```
File load
  → [if checkbox] parse_filename() → pre-fill Key/BPM/Tag, clean base name
  → analyze_file() → {key, camelot, bpm, confidence, stem_type, description}
  → build_filename() → preview column
  → [Rename All] rename_file() + write_metadata()
  → [Export...] ExportDialog → exporter.export_files()
```

---

## Section 1: Smart Name Parser

**File:** `src/renamer.py`

### `parse_filename(stem: str) -> dict`

Regex patterns applied in order to the raw stem name (no extension):

```python
PATTERNS = {
    'tag': r'@(\w+)',
    'bpm': r'\b(\d{2,3})\s*(?:BPM|bpm)\b',
    'key': r'\b([A-G][#b]?(?:maj|min))\b',
}
```

Returns:
```python
{
    'tag':        'BZS',       # or None
    'bpm':        148.0,       # or None
    'key':        'G#min',     # or None
    'clean_name': 'drain 120', # tokens stripped, whitespace normalized
}
```

### Rules
- Multiple BPM matches → use first, ignore rest
- No match on a field → field stays `—` / empty, not overwritten
- `clean_name` has matched tokens removed, leading/trailing separators (`_`, `-`, space) stripped

### UI
- Checkbox `"Parse existing filename"` left of Producer Tag input
- Active at load time → parse immediately, pre-fill Key/BPM/Tag cells
- Changing checkbox state after load → re-process all rows

---

## Section 2: Extended Analyzer

**File:** `src/analyzer.py`

### `analyze_file(path: str) -> dict`

Extended return value:

```python
{
    'key':         'G#min',
    'camelot':     '1A',
    'bpm':         148.0,
    'confidence':  0.87,          # 0.0–1.0
    'stem_type':   'drums',       # see below
    'description': 'Percussive, dark, 148 BPM, G#min',
}
```

### Camelot Mapping

Static lookup table (24 entries). Examples:
```
C maj  → 8B    C min  → 5A
G maj  → 9B    G min  → 6A
G#/Ab maj → 4B  G#/Ab min → 1A
...
```

### Confidence Score

Derived from Krumhansl-Schmuckler dot-product score:
- Normalize best score against worst possible score → 0.0–1.0
- Displayed in UI as percentage, color-coded: green (>0.75), yellow (0.5–0.75), red (<0.5)

### Stem Type Heuristics

All features computed from existing `y, sr` — no re-load:

| Condition | → stem_type |
|-----------|-------------|
| Sub energy (< 120 Hz) > 60% of total | `808` |
| Onset rate > 8/s AND spectral centroid < 2000 Hz | `kick` |
| Onset rate > 12/s AND spectral centroid > 4000 Hz | `hihat` |
| Onset rate > 6/s AND centroid 2000–6000 Hz | `snare` |
| Onset rate < 4/s AND tonal (chroma energy high) | `melodic` |
| Otherwise | `unknown` |

### Description Template

```python
brightness = 'bright' if centroid > 3000 else 'dark'
character  = 'percussive' if onset_rate > 6 else 'tonal'
description = f"{character.capitalize()}, {brightness}, {int(bpm)} BPM, {key}"
# → "Percussive, dark, 148 BPM, G#min"
```

### UI Changes (Table)

Two new columns inserted after BPM:

| Col | Label | Width | Editable |
|-----|-------|-------|----------|
| COL_CAMELOT | Camelot | 60px fixed | No |
| COL_CONF | Conf. | 55px fixed | No |

`Conf.` cell foreground: green `#5cb85c` / yellow `#f0ad4e` / red `#ff4444` based on score.

---

## Section 3: Metadata Writer

**File:** `src/metadata.py`

### `write_metadata(path: str, data: dict) -> None`

```python
data = {
    'title':   str,   # clean base name (parse_filename clean_name or raw stem)
    'artist':  str,   # producer tag
    'bpm':     str,   # integer string e.g. "148"
    'key':     str,   # e.g. "G#min"
    'comment': str,   # description string
    'date':    str,   # ISO date "2026-05-05"
}
```

### Format Support

| Format | Library | Tag system | BPM field |
|--------|---------|-----------|-----------|
| `.mp3` | mutagen | ID3v2.4 | `TBPM` |
| `.flac` | mutagen | VorbisComment | `BPM` |
| `.wav` | mutagen | RIFF INFO | `IBPM` |
| `.aiff` / `.aif` | mutagen | ID3 | `TBPM` |
| `.ogg` | mutagen | VorbisComment | `BPM` |

### Behavior
- Called automatically after `rename_file()` in rename batch
- Errors are caught silently, logged to status bar tooltip (no dialog, no abort)
- Unsupported formats → skip silently

---

## Section 4: Folder Export

**File:** `src/exporter.py`

### `export_files(rows: list, dest_dir: str, structure: str, mode: str) -> tuple[int, list]`

```python
rows      # list of dicts: {path, stem_type, bpm, key, description}
structure # 'bpm_range' | 'stem_type' | 'source_folder'
mode      # 'copy' | 'move'
# returns (success_count, error_list)
```

### BPM Range Buckets

| Range | Folder name |
|-------|------------|
| < 100 | `Sub-100` |
| 100–119 | `100-119 BPM` |
| 120–139 | `120-139 BPM` |
| 140–159 | `140-159 BPM` |
| ≥ 160 | `160plus BPM` |

BPM unknown (not analyzed) → `Unsorted/`

### Stem Type Folder Names

```
kick → Kicks/    snare → Snares/    hihat → Hihats/
808  → 808s/     melodic → Melodics/   unknown → Unsorted/
```

### Source Folder

Uses `os.path.basename(os.path.dirname(original_path))` as subfolder name.

### UI — Export Dialog (`QDialog`)

```
┌─────────────────────────────────────┐
│  Export Files                       │
├─────────────────────────────────────┤
│  Destination:  [E:\Exports\...]  [Browse] │
│  Structure:    [BPM Range        ▾] │
│  Mode:         ● Copy   ○ Move      │
├─────────────────────────────────────┤
│              [Cancel]  [Export]     │
└─────────────────────────────────────┘
```

- `Export...` button added to button row, right of `Rename All`
- Enabled only when files are loaded
- After export: status `"42 files exported to E:\Exports\"`
- On partial failure: `"38 exported, 4 failed"` + warning dialog with error list

---

## Bonus Features (v2 scope)

| Feature | Where |
|---------|-------|
| Camelot column | Table, analyzer |
| Confidence score (color-coded) | Table, analyzer |

### Deferred to v3
- Audio preview (QMediaPlayer)
- Waveform thumbnail
- Naming template engine
- Undo rename batch
- Export CSV/JSON report
- Duplicate detector (same BPM+Key highlight)
- FL Studio folder preset

---

## Dependencies

Add to `requirements.txt`:
```
mutagen>=1.47
```

All other dependencies (librosa, aubio, numpy, PyQt5) already present.

---

## Testing

Manual test matrix:
- MP3 with `@tag 148BPM G#min` in name → parse checkbox pre-fills correctly
- WAV with no metadata → metadata written after rename
- 20 files dropped → export to BPM Range → correct subfolder distribution
- File with BPM not analyzed → exported to `Unsorted/`
- Confidence < 0.5 → red cell color
