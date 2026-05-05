# TODOS — R16 AudioTool
> Bestätigte Aufgaben. Reihenfolge = Priorität.

---

## In Progress / Nächstes

- [ ] **GPU-Detect beim Start** — `torch.cuda.is_available()` + VRAM prüfen, in `settings.json` speichern
- [ ] **Setup-Dialog** — beim ersten Start fragen: GPU ja/nein/auto, CPU-only Modus wenn nein
- [ ] **GPU-Features ausgrauen** — Stem Sep / Apollo / AudioSR / VibeVoice in UI disabled wenn kein GPU-Modus
- [ ] **Modelle lazy downloaden** — nicht beim Install, erst beim ersten Nutzen

---

## Naming Format

- [x] Square-bracket Tag-Block als Pattern-Token `{[tags]}` — z.B. `[analog, wavy, don]`
- [x] Mehrere @Producer-Tags in UI + Pattern
- [x] BPM-Format wählbar: `130` / `130bpm` / `(130bpm)`

---

## Genre / Style Tags

- [x] Multi-Select Dropdown für Style-Tags → in `[...]` Block
- [x] Freitext-Eingabe + eigene Tags speichern

---

## Done

- [x] Multi-Beat Drop fix — append statt replace, dedup per Pfad
