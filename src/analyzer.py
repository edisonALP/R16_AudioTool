import numpy as np
import librosa
import aubio
import tempfile
import os
import soundfile as sf

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _to_music_range(bpm: float) -> float:
    while 0 < bpm < 80:
        bpm *= 2
    while bpm > 180:
        bpm /= 2
    return bpm


def detect_bpm(path: str, y=None, sr=None) -> float:
    if y is None:
        y, sr = librosa.load(path, sr=44100, mono=True)

    hop = 256
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop, aggregate=np.median)

    # Tempogram: gives energy at each tempo over time — much more robust than beat tracking
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=hop, win_length=384)

    # Sum tempogram over time → aggregate tempo strength
    tempo_energy = tg.mean(axis=1)
    bpm_axis     = librosa.tempo_frequencies(len(tempo_energy), sr=sr, hop_length=hop)

    # Mask to musical range 80–180 BPM
    mask = (bpm_axis >= 80) & (bpm_axis <= 180)
    if not mask.any():
        mask = (bpm_axis >= 60) & (bpm_axis <= 200)

    peak_idx = np.argmax(tempo_energy[mask])
    bpm      = float(bpm_axis[mask][peak_idx])

    return round(bpm, 1)


def detect_key(y, sr) -> str:
    if sr != 22050:
        y  = librosa.resample(y, orig_sr=sr, target_sr=22050)
        sr = 22050

    chroma      = librosa.feature.chroma_cens(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    if chroma_mean.sum() > 0:
        chroma_mean = chroma_mean / chroma_mean.sum()

    best_key   = 'C'
    best_mode  = 'maj'
    best_score = -np.inf

    for i in range(12):
        maj  = np.roll(_MAJOR, i);  maj  = maj  / maj.sum()
        min_ = np.roll(_MINOR, i);  min_ = min_ / min_.sum()

        if (s := float(np.dot(chroma_mean, maj))) > best_score:
            best_score, best_key, best_mode = s, NOTES[i], 'maj'
        if (s := float(np.dot(chroma_mean, min_))) > best_score:
            best_score, best_key, best_mode = s, NOTES[i], 'min'

    return f"{best_key}{best_mode}"


def analyze_file(path: str) -> dict:
    y, sr = librosa.load(path, sr=44100, mono=True)
    bpm   = detect_bpm(path, y, sr)
    key   = detect_key(y, sr)
    return {'bpm': bpm, 'key': key}
