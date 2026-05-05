import pytest
from src.presets import PRESETS
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


def test_parse_key_with_trailing_number():
    r = parse_filename("fiss 140 @beatsexuell d#min_1")
    assert r['key'] == 'D#min'


def test_parse_tag_stops_at_space():
    r = parse_filename("drain @fred_g 148BPM G#min")
    assert r['tag'] == 'fred_g'
    assert r['bpm'] == 148.0
    assert r['key'] == 'G#min'


def test_build_classic():
    pattern = PRESETS["Classic"]
    name = build_filename("drain", "G#min", 148.0, "BZS", ".wav", pattern)
    assert name == "drain_G#min_148BPM_BZS.wav"


def test_build_classic_integer_bpm():
    pattern = PRESETS["Classic"]
    name = build_filename("loop", "Cmin", 120.0, "BZS", ".wav", pattern)
    assert name == "loop_Cmin_120BPM_BZS.wav"


def test_build_classic_float_bpm():
    pattern = PRESETS["Classic"]
    name = build_filename("loop", "Cmin", 120.2, "BZS", ".wav", pattern)
    assert name == "loop_Cmin_120.2BPM_BZS.wav"


def test_build_splice():
    pattern = PRESETS["Splice"]
    name = build_filename("drain", "C#min", 120.0, "BZS", ".mp3", pattern)
    assert name == "BZS_drain_120_C#min.mp3"


def test_build_looperman():
    pattern = PRESETS["Looperman"]
    name = build_filename("drain", "C#min", 120.0, "BZS", ".wav", pattern)
    assert name == "drain_120bpm_C#min.wav"


def test_build_minimal():
    pattern = PRESETS["Minimal"]
    name = build_filename("drain", "C#min", 120.0, "BZS", ".wav", pattern)
    assert name == "drain_C#min_120.wav"


def test_build_skips_empty_key():
    pattern = PRESETS["Classic"]
    name = build_filename("loop", "", 120.0, "BZS", ".wav", pattern)
    assert name == "loop_120BPM_BZS.wav"


def test_build_skips_empty_tag():
    pattern = PRESETS["Classic"]
    name = build_filename("loop", "Cmin", 120.0, "", ".wav", pattern)
    assert name == "loop_Cmin_120BPM.wav"


def test_build_skips_zero_bpm():
    pattern = PRESETS["Classic"]
    name = build_filename("loop", "Cmin", 0.0, "BZS", ".wav", pattern)
    assert name == "loop_Cmin_BZS.wav"


def test_build_custom_pattern():
    pattern = [("key", ""), ("name", ""), ("tag", "")]
    name = build_filename("loop", "Amin", 120.0, "BZS", ".wav", pattern)
    assert name == "Amin_loop_BZS.wav"


# --- New token tests ---

def test_build_style_tags_token():
    pattern = [("style_tags", ""), ("name", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern,
                          style_tags=["analog", "wavy"])
    assert name == "[analog, wavy]_beat.wav"


def test_build_style_tags_empty():
    pattern = [("style_tags", ""), ("name", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern, style_tags=[])
    assert name == "beat.wav"


def test_build_style_tags_strips_blank_entries():
    pattern = [("style_tags", ""), ("name", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern,
                          style_tags=["analog", "  ", "wavy"])
    assert name == "[analog, wavy]_beat.wav"


def test_build_producers_single():
    pattern = [("name", ""), ("producers", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern,
                          producers=["beatsexuell"])
    assert name == "beat_@beatsexuell.wav"


def test_build_producers_multi():
    pattern = [("name", ""), ("producers", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern,
                          producers=["beatsexuell", "R16Studios"])
    assert name == "beat_@beatsexuell_@R16Studios.wav"


def test_build_producers_empty():
    pattern = [("name", ""), ("producers", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern, producers=[])
    assert name == "beat.wav"


def test_build_bpm_paren():
    pattern = [("name", ""), ("bpm_paren", "")]
    name = build_filename("beat", "", 130.0, "", ".wav", pattern)
    assert name == "beat_(130bpm).wav"


def test_build_bpm_paren_empty_when_no_bpm():
    pattern = [("name", ""), ("bpm_paren", "")]
    name = build_filename("beat", "", 0, "", ".wav", pattern)
    assert name == "beat.wav"


def test_build_loop_pool_preset():
    from src.presets import PRESETS
    pattern = PRESETS["Loop Pool"]
    name = build_filename("numb", "", 130.0, "", ".mp3", pattern,
                          style_tags=["analog", "don"],
                          producers=["beatsexuell", "R16Studios"])
    assert name == "[analog, don]_numb_130bpm_@beatsexuell_@R16Studios.mp3"


def test_build_backward_compat_no_new_params():
    """Old callers without style_tags/producers still work."""
    pattern = [("name", ""), ("key", ""), ("bpm_raw", "BPM"), ("tag", "")]
    name = build_filename("drain", "G#min", 148.0, "BZS", ".wav", pattern)
    assert name == "drain_G#min_148BPM_BZS.wav"
