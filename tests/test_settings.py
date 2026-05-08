import json, os, pytest
import src.settings as sett


def test_load_defaults_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(sett, "_path", lambda: str(tmp_path / "settings.json"))
    data = sett.load()
    assert data["style_tags"] == []
    assert data["custom_tags"] == []
    assert data["producers"] == ["beatsexuell"]


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(sett, "_path", lambda: str(tmp_path / "settings.json"))
    sett.save({"style_tags": ["analog", "wavy"], "custom_tags": [], "producers": ["BZS"]})
    data = sett.load()
    assert data["style_tags"] == ["analog", "wavy"]
    assert data["producers"] == ["BZS"]


def test_load_merges_missing_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(sett, "_path", lambda: str(tmp_path / "settings.json"))
    path = tmp_path / "settings.json"
    path.write_text('{"style_tags": ["don"]}', encoding="utf-8")
    data = sett.load()
    assert data["style_tags"] == ["don"]
    assert data["producers"] == ["beatsexuell"]


def test_load_handles_corrupt_json(tmp_path, monkeypatch):
    monkeypatch.setattr(sett, "_path", lambda: str(tmp_path / "settings.json"))
    (tmp_path / "settings.json").write_text("NOT JSON", encoding="utf-8")
    data = sett.load()
    assert data["style_tags"] == []
    assert data["producers"] == ["beatsexuell"]
    assert data["gpu_mode"] == "auto"
    assert data["gpu_setup_done"] is False


def test_gpu_defaults_present(tmp_path, monkeypatch):
    monkeypatch.setattr(sett, "_path", lambda: str(tmp_path / "settings.json"))
    data = sett.load()
    assert data["gpu_mode"] == "auto"
    assert data["gpu_setup_done"] is False


def test_gpu_setup_done_survives_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(sett, "_path", lambda: str(tmp_path / "settings.json"))
    sett.save({"gpu_mode": "cpu", "gpu_setup_done": True,
               "style_tags": [], "custom_tags": [], "producers": []})
    data = sett.load()
    assert data["gpu_mode"] == "cpu"
    assert data["gpu_setup_done"] is True
