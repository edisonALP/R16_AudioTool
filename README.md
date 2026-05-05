<div align="center">
  <h1>🎛️ R16 AudioTool</h1>
  <p><b>The ultimate FL Studio companion tool for producers and beatmakers.</b></p>
  
  ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
  ![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=flat-square&logo=qt)
  ![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)
</div>

---

## 🎵 Overview

**R16 AudioTool** is a lightweight desktop application designed to streamline the workflow of music producers. It automatically analyzes your exported audio stems, detects their **Key** and **BPM**, and renames them by baking the metadata directly into the filename — using any naming format you choose.

**Before:**
`Melody_Loop.wav`  
`Drums_Full.wav`

**After (Classic):**
`Melody_Loop_D#min_140BPM_BZS.wav`  
`Drums_Full_140BPM_BZS.wav`

**After (Splice):**
`BZS_Melody_Loop_140_D#min.wav`  
`BZS_Drums_Full_140.wav`

---

## ✨ Features

- 🎹 **Advanced Key Detection:** Krumhansl-Schmuckler algorithm via `chroma_cens` for accurate key detection, robust against complex timbres.
- 🥁 **Smart BPM Detection:** Tempogram analysis tailored for Trap, Drill, and syncopated beats.
- 🏷️ **Flexible Naming Patterns:** Choose from built-in platform presets or build a custom token sequence — no typing required.
- 🖱️ **Drag & Drop Workflow:** Drop entire folders or individual stems directly into the app.
- ✏️ **Editable Metadata:** Review and correct Key, BPM, and Producer Tag before committing changes.
- 👀 **Live Preview:** Instantly see the new filenames as you adjust settings.
- 🚀 **Non-Destructive & Safe:** Files only rename after your explicit confirmation.
- 💻 **Cross-Platform:** Windows, macOS, and Linux.

---

## 🏷️ Naming Pattern Presets

R16 AudioTool ships with platform-specific presets. Click **▶ Naming Pattern** to expand the bar, then switch presets or build your own by clicking token chips:

| Preset | Format | Example |
|--------|--------|---------|
| **Classic** | `name_key_bpmBPM_tag` | `drain_C#min_120BPM_BZS.wav` |
| **Splice** | `tag_name_bpm_key` | `BZS_drain_120_C#min.wav` |
| **Looperman** | `name_bpmbpm_key` | `drain_120bpm_C#min.wav` |
| **Minimal** | `name_key_bpm` | `drain_C#min_120.wav` |
| **Custom** | your choice | any order |

Available tokens: `Name` · `Key` · `BPM` · `BPM#` (plain number) · `Tag`

---

## 🛠️ Supported Formats
`.wav` · `.mp3` · `.flac` · `.aiff` · `.aif` · `.ogg`

---

## 🚀 Installation

### Windows
```bash
git clone https://github.com/edisonALP/R16_AudioTool.git
cd R16_AudioTool
pip install -r requirements.txt
```

### macOS / Linux
```bash
git clone https://github.com/edisonALP/R16_AudioTool.git
cd R16_AudioTool
pip3 install -r requirements.txt
```

---

## 🎮 Usage

```bash
python main.py
```

### Recommended Workflow for FL Studio:
1. **Export Stems:** *File → Export → Wave file → Split mixer tracks*
2. **Import:** Drag & drop your stem folder into R16 AudioTool
3. **Choose Pattern:** Click **▶ Naming Pattern** and pick a preset (e.g. Splice)
4. **Analyze:** Click **"Analyze All"** to detect Key and BPM
5. **Tag:** Enter your **Producer Tag** — applies to all stems
6. **Review:** Double-click any cell to correct values
7. **Rename:** Click **"Rename All Files"**

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `PyQt5` | Dark-theme GUI |
| `librosa` | Audio analysis & Key detection |
| `aubio` | Beat tracking |
| `numpy` | DSP operations |
| `soundfile` | Audio I/O |
| `scipy` | Signal processing |
| `mutagen` | Metadata writing |

---

## 📂 Project Structure

```text
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
└── src/
    ├── analyzer.py      # BPM + Key detection
    ├── renamer.py       # Filename building and renaming
    ├── presets.py       # Naming pattern preset definitions
    ├── pattern_bar.py   # Collapsible naming pattern UI widget
    ├── main_window.py   # Main GUI
    └── styles.py        # Dark theme stylesheet
```

---

<div align="center">
  <p>Made with ❤️ by <b>R16</b></p>
</div>
