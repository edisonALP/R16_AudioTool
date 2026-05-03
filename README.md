<div align="center">
  <h1>🎛️ R16 Stem Tool</h1>
  <p><b>The ultimate FL Studio companion tool for producers and beatmakers.</b></p>
  
  ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
  ![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=flat-square&logo=qt)
  ![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)
</div>

---

## 🎵 Overview

**Stem Tool**  is a lightweight, cross-platform desktop application designed to streamline the workflow of music producers. It automatically analyzes your exported audio stems, detects their **Key** and **BPM**, and effortlessly renames them by baking the metadata directly into the filename.

**Before:**
`Melody_Loop.wav`  
`Drums_Full.wav`

**After:**
`Melody_Loop_D#min_140BPM_BZS.wav`  
`Drums_Full_140BPM_BZS.wav`

---

## ✨ Features

- 🎹 **Advanced Key Detection:** Utilizes the Krumhansl-Schmuckler algorithm via `chroma_cens` for highly accurate key detection, robust against complex timbres.
- 🥁 **Smart BPM Detection:** Tempogram analysis tailored to handle complex modern rhythms like Trap, Drill, and syncopated beats.
- 🖱️ **Drag & Drop Workflow:** Seamlessly drop entire folders or individual stems directly into the application.
- ✏️ **Editable Metadata:** Review and manually adjust Key, BPM, and Producer Tag in a clean table interface before committing changes.
- 👀 **Live Preview:** Instantly see what the new filenames will look like as you type.
- 🚀 **Non-Destructive & Safe:** Files are only renamed after your explicit confirmation.
- 💻 **Cross-Platform:** Works out-of-the-box on Windows, macOS, and Linux.

---

## 🛠️ Supported Formats
`.wav` · `.mp3` · `.flac` · `.aiff` · `.aif` · `.ogg`

---

## 🚀 Installation

### Windows
```bash
# Clone the repository
git clone https://github.com/edisonALP/R16_Metafinder.git
cd R16_Metafinder

# Install dependencies
pip install -r requirements.txt

# Or simply double-click the provided script:
# install.bat
```

### macOS / Linux
```bash
# Clone the repository
git clone https://github.com/edisonALP/R16_Metafinder.git
cd R16_Metafinder

# Install dependencies
pip3 install -r requirements.txt

# Or simply run the provided script:
# sh install.sh
```

---

## 🎮 Usage

Launch the tool by running:
```bash
python main.py
```

### 💡 Recommended Workflow for FL Studio:
1. **Export Stems:** In FL Studio, go to *File → Export → Wave file → Split mixer tracks*.
2. **Import:** Drag & drop your newly exported stem folder into the **BZS Stem Tool**.
3. **Analyze:** Click **"Analyze All"** to automatically calculate the Key and BPM for every file.
4. **Tag:** Enter your custom **Producer Tag** (e.g., "BZS"). It will apply to all loaded stems.
5. **Review:** Check the generated values in the table. Double-click any cell to make manual corrections.
6. **Rename:** Click **"Rename All Files"** to apply the new filenames instantly.

---

## 📦 Dependencies

This tool relies on powerful open-source libraries for audio processing and GUI rendering:

| Package | Purpose |
|---------|---------|
| `PyQt5` | Modern Dark-Theme GUI |
| `librosa` | Core audio analysis & Key detection |
| `aubio` | Advanced beat tracking |
| `numpy` | Matrix and DSP operations |
| `soundfile` | Fast Audio I/O operations |
| `scipy` | Mathematical signal processing |

---

## 📂 Project Structure

```text
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── install.bat          # Windows quick-setup
├── install.sh           # macOS/Linux quick-setup
└── src/
    ├── analyzer.py      # Core DSP logic (BPM + Key)
    ├── renamer.py       # File renaming and formatting logic
    ├── main_window.py   # Main GUI implementation
    └── styles.py        # Dark theme stylesheet
```

---

<div align="center">
  <p>Made with ❤️ by <b>R16</b></p>
</div>
