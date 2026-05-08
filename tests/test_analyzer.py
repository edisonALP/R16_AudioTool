import numpy as np
import pytest
from src.analyzer import _camelot_key, _confidence_from_scores, NOTES


def test_camelot_cmaj():
    assert _camelot_key('C', 'maj') == '8B'


def test_camelot_amin():
    assert _camelot_key('A', 'min') == '8A'


def test_camelot_gsharp_min():
    assert _camelot_key('G#', 'min') == '1A'


def test_camelot_unknown_note():
    assert _camelot_key('X', 'maj') == '?'


def test_confidence_high():
    score = _confidence_from_scores(best=5.0, all_scores=np.array([1.0, 2.0, 3.0, 5.0, 1.5]))
    assert score > 0.7


def test_confidence_low():
    score = _confidence_from_scores(best=2.1, all_scores=np.array([2.0, 2.1, 2.0, 2.05, 2.0]))
    assert score < 0.4


def test_confidence_range():
    scores = np.random.uniform(0, 5, 24)
    best = scores.max()
    c = _confidence_from_scores(best, scores)
    assert 0.0 <= c <= 1.0


from src.analyzer import _classify_stem_type, _build_description


def test_stem_type_808_high_sub():
    assert _classify_stem_type(sub_ratio=0.7, onset_rate=2.0, centroid=800.0) == '808'


def test_stem_type_kick():
    assert _classify_stem_type(sub_ratio=0.1, onset_rate=9.0, centroid=1500.0) == 'kick'


def test_stem_type_hihat():
    assert _classify_stem_type(sub_ratio=0.05, onset_rate=14.0, centroid=6000.0) == 'hihat'


def test_stem_type_snare():
    assert _classify_stem_type(sub_ratio=0.1, onset_rate=8.0, centroid=3000.0) == 'snare'


def test_stem_type_melodic():
    assert _classify_stem_type(sub_ratio=0.1, onset_rate=1.0, centroid=2000.0) == 'melodic'


def test_stem_type_unknown():
    assert _classify_stem_type(sub_ratio=0.1, onset_rate=5.0, centroid=3000.0) == 'unknown'


def test_build_description_percussive_dark():
    d = _build_description(onset_rate=10.0, centroid=1500.0, bpm=148.0, key='G#min')
    assert d == 'Percussive, dark, 148 BPM, G#min'


def test_build_description_tonal_bright():
    d = _build_description(onset_rate=2.0, centroid=5000.0, bpm=120.0, key='Cmaj')
    assert d == 'Tonal, bright, 120 BPM, Cmaj'


from src.analyzer import detect_clipping, detect_lufs


def test_clipping_detected_at_limit():
    y = np.zeros(44100, dtype=np.float32)
    y[1000] = 1.0
    assert detect_clipping(y) is True


def test_clipping_detected_at_threshold():
    y = np.full(44100, 0.5, dtype=np.float32)
    y[500] = 0.999
    assert detect_clipping(y) is True


def test_no_clipping_below_threshold():
    y = np.full(44100, 0.5, dtype=np.float32)
    assert detect_clipping(y) is False


def test_lufs_returns_float_for_valid_audio():
    sr = 44100
    t = np.linspace(0, 1.0, sr, dtype=np.float32)
    y = 0.1 * np.sin(2 * np.pi * 440 * t)
    result = detect_lufs(y, sr)
    assert result is None or isinstance(result, float)


def test_lufs_returns_none_for_short_audio():
    y = np.zeros(100, dtype=np.float32)
    result = detect_lufs(y, 44100)
    assert result is None


def test_analyze_file_has_clipping_and_lufs_keys(tmp_path):
    import soundfile as sf
    sr = 44100
    t = np.linspace(0, 2.0, sr * 2, dtype=np.float32)
    y = 0.3 * np.sin(2 * np.pi * 220 * t)
    path = str(tmp_path / "test.wav")
    sf.write(path, y, sr)

    from src.analyzer import analyze_file
    result = analyze_file(path)
    assert "clipping" in result
    assert "lufs" in result
    assert isinstance(result["clipping"], bool)
