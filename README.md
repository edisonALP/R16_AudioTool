# R16 AudioTool

**FL Studio companion tool for producers.** Analyzes exported stems, detects Key and BPM, renames files with metadata baked into the filename.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=flat-square&logo=qt)
![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)

---

## What it does

**Before:**
```
Melody_Loop.wav
Drums_Full.wav
```

**After (Classic):**
```
Melody_Loop_D#min_140BPM_BZS.wav
Drums_Full_140BPM_BZS.wav
```

**After (Splice):**
```
BZS_Melody_Loop_140_D#min.wav
BZS_Drums_Full_140.wav
```

---

## Features

- **Key Detection** — Krumhansl-Schmuckler algorithm via `chroma_cens`, accurate on complex timbres
- **BPM Detection** — Tempogram analysis tuned for Trap, Drill, and syncopated beats
- **Naming Patterns** — Built-in platform presets or fully custom token order
- **Style Tags** — One-click genre tags (trap, drill, phonk, ambient…) via `[Tags]` token
- **Multi-Producer Credits** — Up to 3 names, auto-formatted as `@Name1_@Name2`
- **Drag & Drop** — Drop folders or single files directly into the app
- **Editable Metadata** — Correct Key, BPM, or tag before renaming
- **Live Preview** — See new filenames update in real time
- **Non-Destructive** — Files only rename after explicit confirmation
- **Cross-Platform** — Windows and macOS

---

## Naming Presets

| Preset | Format | Example |
|--------|--------|---------|
| Classic | `name_key_bpmBPM_tag` | `drain_C#min_120BPM_BZS.wav` |
| Splice | `tag_name_bpm_key` | `BZS_drain_120_C#min.wav` |
| Looperman | `name_bpmbpm_key` | `drain_120bpm_C#min.wav` |
| Minimal | `name_key_bpm` | `drain_C#min_120.wav` |
| Loop Pool | `[tags]_name_bpmbpm_@producers` | `[trap, dark]_drain_120bpm_@BZS.wav` |
| Custom | your choice | any order |

**Available tokens:** `Name` · `Key` · `BPM` · `BPM#` · `bpm` · `(BPM)` · `Tag` · `[Tags]` · `@Producers`

---

## Supported Formats

`.wav` · `.mp3` · `.flac` · `.aiff` · `.aif` · `.ogg`

---

## Download

Go to [Releases](https://github.com/edisonALP/R16_AudioTool/releases) and download the latest version for your platform.

- **Windows:** `R16_AudioTool.exe`
- **macOS:** `R16_AudioTool-macOS.zip` → unzip → drag to Applications → right-click → Open (first launch only)

---

## Run from source

**Windows:**
```bash
git clone https://github.com/edisonALP/R16_AudioTool.git
cd R16_AudioTool
pip install -r requirements.txt
python main.py
```

**macOS / Linux:**
```bash
git clone https://github.com/edisonALP/R16_AudioTool.git
cd R16_AudioTool
pip3 install -r requirements.txt
python3 main.py
```

---

## Workflow (FL Studio)

1. Export stems: *File → Export → Wave file → Split mixer tracks*
2. Drag & drop stem folder into R16 AudioTool
3. Pick a naming preset under **Naming Pattern**
4. Set genre tags and producer name(s) under **Style Tags & Producers**
5. Click **Analyze All**
6. Correct any values by double-clicking a cell
7. Click **Rename All Files**

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `PyQt5` | GUI |
| `librosa` | Audio analysis & key detection |
| `aubio` | Beat tracking |
| `numpy` | DSP |
| `soundfile` | Audio I/O |
| `scipy` | Signal processing |
| `mutagen` | Metadata writing |

---

Made by **R16**
