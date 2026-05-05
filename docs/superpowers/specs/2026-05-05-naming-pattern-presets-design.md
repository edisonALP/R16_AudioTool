# Naming Pattern Presets — Design Spec
Date: 2026-05-05

## Goal
Replace hardcoded `{name}_{key}_{bpm}BPM_{tag}` filename format with a flexible,
non-technical UI that lets users pick platform presets or build a custom token sequence.

## Presets

| Preset    | Token Order                        | Example Output              |
|-----------|------------------------------------|-----------------------------|
| Splice    | tag _ name _ bpm_raw _ key         | `BZS_drain_120_C#min.mp3`   |
| Looperman | name _ bpm_raw+bpm _ key           | `drain_120bpm_C#min.mp3`    |
| Classic   | name _ key _ bpm+BPM _ tag         | `drain_C#min_120BPM_BZS.mp3`|
| Minimal   | name _ key _ bpm_raw               | `drain_C#min_120.mp3`       |
| Custom    | user-defined                       | any                         |

## Token IDs

| ID       | Value              | Notes                          |
|----------|--------------------|--------------------------------|
| name     | clean filename stem | @tags and known tokens removed |
| key      | e.g. C#min         | skipped if empty               |
| bpm      | e.g. 120BPM        | suffix appended directly       |
| bpm_raw  | e.g. 120           | plain number, no suffix        |
| tag      | e.g. BZS           | skipped if empty               |

Tokens with empty/zero values are silently skipped.
Separator between all tokens: `_`.

## Data Model

`src/presets.py` — pure data, no Qt:
```python
# Each token: (token_id, suffix)
PRESETS: dict[str, list[tuple[str, str]]] = {
    "Splice":    [("tag",""), ("name",""), ("bpm_raw",""), ("key","")],
    "Looperman": [("name",""), ("bpm_raw","bpm"), ("key","")],
    "Classic":   [("name",""), ("key",""), ("bpm_raw","BPM"), ("tag","")],
    "Minimal":   [("name",""), ("key",""), ("bpm_raw","")],
    "Custom":    [],
}
```

## API Change: `build_filename`

```python
# renamer.py
def build_filename(
    clean_name: str,
    key: str,
    bpm: float,
    tag: str,
    ext: str,
    pattern: list[tuple[str, str]],
) -> str:
    ...
```

Token resolution:
- `name` → `clean_name`
- `key` → `key`
- `bpm` → `f"{int(bpm) if bpm==int(bpm) else bpm}{suffix}"`
- `bpm_raw` → `f"{int(bpm) if bpm==int(bpm) else bpm}{suffix}"`
- `tag` → `tag`

Skip token if resolved value is falsy (`""`, `0`, `0.0`).
Join non-empty tokens with `_`, append `ext`.

## UI Component: `NamingPatternBar`

New file: `src/pattern_bar.py`, class `NamingPatternBar(QWidget)`.

### Layout (collapsible)

```
Collapsed:  ▶  Naming Pattern: Splice
Expanded:   ▼  Naming Pattern
            [Splice ▼]   Available: [Name] [Key] [BPM] [BPM#] [Tag]
            Active:      [Name ×] [Key ×] [BPM ×] [Tag ×]
            Preview:     drain_C#min_120BPM_BZS.mp3
```

### Behaviour
- Toggle button collapses/expands section
- Preset dropdown: selecting a named preset overwrites active sequence
- Selecting "Custom" in dropdown: keeps current sequence editable
- Modifying active sequence while a named preset is selected → auto-switches dropdown to "Custom"
- Click token in Available → appends to active sequence
- Click × on active token → removes it
- Any change emits `pattern_changed` signal → `MainWindow._update_all_previews()`

### Signals
```python
pattern_changed = pyqtSignal()
```

### Public API
```python
def current_pattern(self) -> list[tuple[str, str]]: ...
```

## Integration in `main_window.py`

1. Instantiate `NamingPatternBar`, insert between header and table in layout
2. Connect `pattern_bar.pattern_changed` → `_update_all_previews`
3. In `_update_preview(row)`: pass `self.pattern_bar.current_pattern()` to `build_filename`

## Files Changed

| File                  | Change                                      |
|-----------------------|---------------------------------------------|
| `src/presets.py`      | NEW — preset definitions                    |
| `src/pattern_bar.py`  | NEW — NamingPatternBar widget               |
| `src/renamer.py`      | modify `build_filename` signature + logic   |
| `src/main_window.py`  | integrate NamingPatternBar, update call site|
| `tests/test_renamer.py` | add cases for pattern-based build_filename|

## Out of Scope
- Persisting custom pattern across sessions (can be added later)
- Drag & drop reordering of active tokens (can be added later)
- Per-file pattern override
