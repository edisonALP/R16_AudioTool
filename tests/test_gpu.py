import platform
import sys
from unittest.mock import patch, MagicMock

import src.gpu as gpu


def test_returns_dict_with_required_keys():
    result = gpu.detect_gpu()
    assert set(result.keys()) == {"available", "backend", "name", "vram_gb"}


def test_no_gpu_when_all_detection_fails(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "machine", lambda: "AMD64")
    with patch("src.gpu._detect_nvidia", return_value=None):
        result = gpu.detect_gpu()
    assert result == {"available": False, "backend": "none", "name": "", "vram_gb": None}


def test_nvidia_detection(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "machine", lambda: "AMD64")
    nvidia_info = {"available": True, "backend": "cuda", "name": "RTX 4070", "vram_gb": 12.0}
    with patch("src.gpu._detect_nvidia", return_value=nvidia_info):
        result = gpu.detect_gpu()
    assert result["backend"] == "cuda"
    assert result["name"] == "RTX 4070"
    assert result["vram_gb"] == 12.0


def test_apple_silicon_detection(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "machine", lambda: "arm64")
    with patch("src.gpu._detect_apple_silicon_vram", return_value=16.0):
        result = gpu.detect_gpu()
    assert result["available"] is True
    assert result["backend"] == "mps"
    assert result["name"] == "Apple Silicon"
    assert result["vram_gb"] == 16.0


def test_detect_gpu_never_raises(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "machine", lambda: "AMD64")
    with patch("src.gpu._detect_nvidia", side_effect=RuntimeError("boom")):
        result = gpu.detect_gpu()
    assert result["available"] is False


def test_pynvml_path():
    pynvml_mock = MagicMock()
    device_mock = MagicMock()
    mem_mock = MagicMock()
    mem_mock.total = 12 * 1024 ** 3
    pynvml_mock.nvmlDeviceGetMemoryInfo.return_value = mem_mock
    pynvml_mock.nvmlDeviceGetName.return_value = b"RTX 4070"
    pynvml_mock.nvmlDeviceGetHandleByIndex.return_value = device_mock

    with patch.dict(sys.modules, {"pynvml": pynvml_mock}):
        result = gpu._detect_nvidia_via_pynvml()

    assert result is not None
    assert result["name"] == "RTX 4070"
    assert abs(result["vram_gb"] - 12.0) < 0.1
