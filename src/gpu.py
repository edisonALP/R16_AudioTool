import platform
import subprocess


def detect_gpu() -> dict:
    try:
        system = platform.system()
        if system == "Darwin":
            if platform.machine() == "arm64":
                return {
                    "available": True,
                    "backend": "mps",
                    "name": "Apple Silicon",
                    "vram_gb": _detect_apple_silicon_vram(),
                }
            # Intel Mac: no MPS, no CUDA
            return {"available": False, "backend": "none", "name": "Intel Mac", "vram_gb": None}
        if system == "Windows":
            nvidia = _detect_nvidia()
            if nvidia:
                return nvidia
    except Exception:
        pass
    return {"available": False, "backend": "none", "name": "", "vram_gb": None}


def _detect_nvidia() -> dict | None:
    result = _detect_nvidia_via_pynvml()
    if result:
        return result
    return _detect_nvidia_via_smi()


def _detect_nvidia_via_pynvml() -> dict | None:
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        raw_name = pynvml.nvmlDeviceGetName(handle)
        name = raw_name.decode() if isinstance(raw_name, bytes) else raw_name
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        vram_gb = round(mem.total / (1024 ** 3), 1)
        return {"available": True, "backend": "cuda", "name": name, "vram_gb": vram_gb}
    except Exception:
        return None


def _detect_nvidia_via_smi() -> dict | None:
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            timeout=5, stderr=subprocess.DEVNULL, text=True,
        ).strip().splitlines()[0]
        parts = [p.strip() for p in out.split(",")]
        name = parts[0]
        vram_gb = round(int(parts[1]) / 1024, 1)
        return {"available": True, "backend": "cuda", "name": name, "vram_gb": vram_gb}
    except Exception:
        return None


def _detect_apple_silicon_vram() -> float | None:
    try:
        out = subprocess.check_output(
            ["sysctl", "-n", "hw.memsize"], timeout=5, text=True
        ).strip()
        return round(int(out) / (1024 ** 3), 1)
    except Exception:
        return None
