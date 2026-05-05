# Ideas Backlog — R16 AudioTool
> Überlegungen. Werden stück für stück auf Nutzen + Machbarkeit geprüft.
> Ziel: Producer-Helpertool (Richtung noch offen)
>
> Machbarkeit: 🟢 einfach · 🟡 mittel · 🔴 komplex · ⚫ braucht GPU/Cloud

---

## Fixes & Done
- [x] Multi-Beat Drop — 2. Beat hat 1. ersetzt → jetzt append + dedup

---

## Installation / Setup

GPU-Anforderungen der ⚫ Features:
| Tool | Min VRAM | Mindest-GPU |
|---|---|---|
| UVR5 + BS Roformer | 8 GB | NVIDIA RTX 3060+ |
| UVR5 kleine Modelle | 4 GB | NVIDIA GTX 1660+ |
| Demucs4 HT | 4 GB (CPU: 20x langsamer) | NVIDIA / CPU fallback |
| Apollo Enhancer | 6 GB | NVIDIA CUDA |
| AudioSR | 8 GB+ | NVIDIA CUDA |
| VibeVoice | 6–8 GB | NVIDIA CUDA |
> AMD: kaum CUDA-Support. Apple Silicon: nur Demucs.

Ideen für Installer:
- [ ] GPU-Erkennung beim ersten Start (torch.cuda.is_available() + VRAM abfragen) 🟢
- [ ] Setup-Dialog: "Hast du eine NVIDIA GPU?" → ja/nein/auto-detect 🟢
- [ ] GPU-Modus: torch + CUDA Pakete installieren (~2–4 GB extra) 🟡
- [ ] CPU-Modus: torch CPU-only, keine CUDA-Deps, kein UVR/Apollo/AudioSR 🟢
- [ ] GPU-Features in UI ausgrauen wenn kein GPU-Modus aktiv 🟢
- [ ] Modelle lazy downloaden (erst beim ersten Nutzen, nicht beim Install) 🟡
- [ ] Config speichern: `gpu_mode: true/false` in settings.json 🟢

---

## Naming Format
Ziel-Pattern aus Loop Pool (Telegram):
```
[style, vibe, ref_artist] beatname BPM @producer1 @producer2.mp3
```
Beispiele gesehen:
- `[analog, don] numb 130bpm @prodf1sh @mlodyhubson.mp3`
- `[ambient, wavy, tecca] uniform 124 @mlodyhubson.mp3`
- `[don, synth, wavy] @1saacdan @mlodyhubson (138bpm) ridges.mp3`
- `[pierre, babybartier] BATTLE 160 MLODYHUBSON.mp3`
- `[melodic, virtual, uzi] match 145 @mlodyhubson @natemorgan.mp3`
- `don,_synth,_yeat,_hxg_say_so_143_Dm_@mlodyhubson_@prodmizo_.mp3`

| Idee | Machbarkeit |
|---|---|
| Square-bracket Tag-Block `{[tags]}` als Pattern-Token | 🟢 |
| Mehrere @Producer-Tags | 🟢 |
| BPM-Format wählbar: `130` / `130bpm` / `(130bpm)` | 🟢 |
| Key optional im Dateinamen (`Dm`, `F#min`) | 🟢 |
| Referenz-Artist im Tag-Block (wie `tecca`, `uzi`) | 🟢 |

---

## Genre / Style Tags

| Idee | Machbarkeit |
|---|---|
| Multi-Select Dropdown → landen im `[...]` Block | 🟢 |
| Freitext + eigene Tags speichern | 🟢 |
| Referenz-Artist als eigenes Feld | 🟢 |
| Auto-Genre via **Essentia** (Python, lokal) | 🟡 |
| Auto-Genre nur als Vorschlag, manuell überschreibbar | 🟡 |

Vorschlag Style-Liste: `analog, don, wavy, ambient, melodic, drill, trap, afro, synth, dark, cinematic, bounce, grimey, plugg, emo, rage, jersey, uk drill, phonk`

---

## Audio Analyse
Aktuell nutzen wir: librosa (BPM/Key via Tempogram + Krumhansl-Schmuckler)

**Essentia** (Open Source, MTG Barcelona) — Tunebat nutzt Essentia.js:
- FFT-basierte Key-Detection
- Onset Detection für BPM
- ML-Modelle für Mood & Energy (Fröhlichkeit, Aggressivität, etc.)
- Python-Version verfügbar → könnte librosa ersetzen oder ergänzen

| Idee | Machbarkeit |
|---|---|
| Fake-Lossless Detection (Upsampling erkennen) | 🟡 |
| Clipping Detection | 🟢 |
| Spektralanalyse-Ansicht (wie Spek) | 🟡 |
| LUFS / Loudness Messung | 🟢 |
| Mood & Energy via Essentia ML | 🟡 |
| BPM/Key aus Spotify API (Tunebat-Ansatz) | 🟡 nur für bekannte Songs |
| Essentia statt/neben librosa für Analysis | 🟡 |

---

## Stem Separation (eigenes Tab / Modul)
Referenzen: [UVR GUI](https://github.com/Anjok07/ultimatevocalremovergui) · [MVSEP](https://mvsep.com/en/algorithms) · [Training](https://github.com/aufr33/Music-Source-Separation-Training)

Beste Combo laut Research:
- **Vocals**: MelBand Roformer + BS Roformer Ensemble (SDR 11.93 — aktuell bester Stand 2025)
- **Multistem 6**: BS Roformer SW (Vocals/Drums/Bass/Guitar/Piano/Other)
- **Alternative**: Demucs4 HT (Meta, kein CUDA zwingend nötig)
- **Film/Sprache**: BandIt v2
- **Drums Detail**: DrumSep

MVSEP Ensemble SDR Vocals:
| Version | SDR |
|---|---|
| 2024.08 | 11.50 |
| 2024.12 | 11.61 |
| 2025.06 (aktuell) | 11.93 |

| Idee | Machbarkeit |
|---|---|
| MVSEP API (Cloud) | 🟡 kostenpflichtig ab X Requests |
| Lokales UVR5 | ⚫ CUDA + ~2GB Modelle |
| Demucs lokal (CPU möglich) | 🔴 langsam ohne GPU |
| Output-Stems auto benennen nach Pattern | 🟢 |

---

## Restaurierung & Extras

| Idee | Machbarkeit |
|---|---|
| Apollo Enhancer — De-Reverb / Restaurierung | ⚫ |
| AudioSR — Super Resolution (Frequenzen wiederherstellen) | ⚫ |
| Whisper — Lyrics aus Vocals transkribieren | 🟡 CPU möglich aber langsam |
| VibeVoice — Voice Cloning / TTS | ⚫ |
| Text-to-Audio (MVSEP hat das auch) | ⚫ |

---

## UI / UX

| Idee | Machbarkeit |
|---|---|
| Mehrere @Producer-Felder | 🟢 ✅ |
| Tab 2: Stem Separation | 🟡 |
| Waveform Preview | 🟡 |
| Drag & Drop Reihenfolge verändern | 🟡 |
| Export als CSV / JSON | 🟢 |
| Loop Pool Sync (Telegram-Ordner watchen) | 🔴 |
| **Export in Ordner nach Tags** — z.B. alle Beats mit "beatsexuell" → Ordner A, mit "beatsexuell+r16" → Ordner B | 🟢 |

---

## Style Tags Skalierung
> Wenn Tags zu viele werden: UI überfüllt sich.

| Idee | Machbarkeit |
|---|---|
| Tags in Kategorien gruppieren (z.B. Mood / Genre / Ref Artist) | 🟡 |
| Suchfeld zum Filtern von Tags | 🟢 |
| Tags als scrollbare Liste statt Chip-Reihe | 🟢 |
| Nur zuletzt benutzte Tags anzeigen, Rest auf "Mehr…" | 🟢 |
| Preset-Sets speichern (z.B. "Loop Pool Set" = analog+don+wavy) | 🟡 |

---

## Referenzen
- Google Doc: https://docs.google.com/document/u/0/d/14TsXICZDRVFxAcTh3HC60HCckUZsTGOnI3Ji-LpyWEg/mobilebasic
- UVR GUI: https://github.com/Anjok07/ultimatevocalremovergui
- Source Sep Training: https://github.com/aufr33/Music-Source-Separation-Training
- MVSEP Algorithmen: https://mvsep.com/en/algorithms
- MVSEP Ensemble: https://mvsep.com/algorithms/10
- Essentia Docs: https://essentia.upf.edu
