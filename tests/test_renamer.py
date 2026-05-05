import pytest
from src.renamer import parse_filename, build_filename, rename_file


def test_parse_tag():
    r = parse_filename("drain 120 @fred_g @beatsexuell")
    assert r['tag'] == 'fred_g'  # first @tag wins


def test_parse_bpm():
    r = parse_filename("fiss 140BPM d#min")
    assert r['bpm'] == 140.0


def test_parse_bpm_lowercase():
    r = parse_filename("beat 128bpm")
    assert r['bpm'] == 128.0


def test_parse_key_minor():
    r = parse_filename("fiss 140BPM d#min")
    assert r['key'] == 'D#min'


def test_parse_key_major():
    r = parse_filename("loop Gmaj 120BPM")
    assert r['key'] == 'Gmaj'


def test_parse_clean_name():
    r = parse_filename("drain 120 @fred_g 148BPM G#min")
    assert r['clean_name'] == 'drain 120'


def test_parse_no_matches():
    r = parse_filename("simple loop")
    assert r['tag'] is None
    assert r['bpm'] is None
    assert r['key'] is None
    assert r['clean_name'] == 'simple loop'


def test_parse_multiple_bpm_uses_first():
    r = parse_filename("beat 120BPM 140BPM")
    assert r['bpm'] == 120.0


def test_build_filename_no_duplicates():
    name = build_filename("drain 120", "G#min", 148.0, "BZS", ".wav")
    assert name == "drain 120_G#min_148BPM_BZS.wav"


def test_parse_key_with_trailing_number():
    r = parse_filename("fiss 140 @beatsexuell d#min_1")
    assert r['key'] == 'D#min'


def test_parse_tag_stops_at_space():
    r = parse_filename("drain @fred_g 148BPM G#min")
    assert r['tag'] == 'fred_g'
    assert r['bpm'] == 148.0
    assert r['key'] == 'G#min'
