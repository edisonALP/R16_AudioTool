import numpy as np
import librosa
import aubio
import tempfile
import os
import soundfile as sf

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


_CAMELOT = {
    (0,  'maj'): '8B',  (1,  'maj'): '3B',  (2,  'maj'): '10B',
    (3,  'maj'): '5B',  (4,  'maj'): '12B', (5,  'maj'): '7B',
    (6,  'maj'): '2B',  (7,  'maj'): '9B',  (8,  'maj'): '4B',
    (9,  'maj'): '11B', (10, 'maj'): '6B',  (11, 'maj'): '1B',
    (0,  'min'): '5A',  (1,  'min'): '12A', (2,  'min'): '7A',
    (3,  'min'): '2A',  (4,  'min'): '9A',  (5,  'min'): '4A',
    (6,  'min'): '11A', (7,  'min'): '6A',  (8,  'min'): '1A',
    (9,  'min'): '8A',  (10, 'min'): '3A',  (11, 'min'): '10A',
}


def _camelot_key(note: str, mode: str) -> str:
    try:
        idx = NOTES.index(note)
    except ValueError:
        return '?'
    return _CAMELOT.get((idx, mode), '?')


def _confidence_from_scores(best: float, all_scores: np.ndarray) -> float:
    rng  = float(all_scores.max() - all_scores.min())
    mx   = float(all_scores.max())
    if mx == 0:
        return 0.5
    return float(np.clip(rng / mx, 0.0, 1.0))


def _classify_stem_type(sub_ratio: float, onset_rate: float, centroid: float) -> str:
    if sub_ratio > 0.6:
        return '808'
    if onset_rate > 12 and centroid > 4000:
        return 'hihat'
    if onset_rate > 8 and centroid < 2000:
        return 'kick'
    if 6 <= onset_rate <= 12 and 2000 <= centroid <= 6000:
        return 'snare'
    if onset_rate < 4:
        return 'melodic'
    return 'unknown'


def _build_description(onset_rate: float, centroid: float, bpm: float, key: str) -> str:
    character = 'Percussive' if onset_rate > 6 else 'Tonal'
    brightness = 'bright' if centroid > 3000 else 'dark'
    return f"{character}, {brightness}, {int(bpm)} BPM, {key}"


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


def detect_key(y, sr) -> tuple:
    """Returns (key_string, confidence) e.g. ('G#min', 0.87)"""
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
    all_scores = []

    for i in range(12):
        maj  = np.roll(_MAJOR, i);  maj  = maj  / maj.sum()
        min_ = np.roll(_MINOR, i);  min_ = min_ / min_.sum()

        s_maj = float(np.dot(chroma_mean, maj))
        s_min = float(np.dot(chroma_mean, min_))
        all_scores.extend([s_maj, s_min])

        if s_maj > best_score:
            best_score, best_key, best_mode = s_maj, NOTES[i], 'maj'
        if s_min > best_score:
            best_score, best_key, best_mode = s_min, NOTES[i], 'min'

    confidence = _confidence_from_scores(best_score, np.array(all_scores))
    return f"{best_key}{best_mode}", confidence


def analyze_file(path: str) -> dict:
    y, sr = librosa.load(path, sr=44100, mono=True)
    bpm   = detect_bpm(path, y, sr)
    key, confidence = detect_key(y, sr)

    if key.endswith('maj'):
        note, mode = key[:-3], 'maj'
    else:
        note, mode = key[:-3], 'min'

    camelot = _camelot_key(note, mode)

    freq_bins = np.fft.rfftfreq(2048, d=1.0 / sr)
    fft_mag   = np.abs(np.fft.rfft(y, n=2048))
    sub_mask  = freq_bins < 120
    sub_ratio = float(fft_mag[sub_mask].sum() / (fft_mag.sum() + 1e-8))

    onsets     = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    duration   = librosa.get_duration(y=y, sr=sr)
    onset_rate = len(onsets) / max(duration, 1.0)

    centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())

    stem_type   = _classify_stem_type(sub_ratio, onset_rate, centroid)
    description = _build_description(onset_rate, centroid, bpm, key)

    return {
        'key':         key,
        'camelot':     camelot,
        'bpm':         bpm,
        'confidence':  round(confidence, 2),
        'stem_type':   stem_type,
        'description': description,
    }
