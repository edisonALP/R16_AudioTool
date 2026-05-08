# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_all, collect_dynamic_libs

aubio_datas, aubio_binaries, aubio_hiddenimports = collect_all('aubio')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=aubio_binaries + collect_dynamic_libs('aubio'),
    datas=[('assets', 'assets')] + aubio_datas,
    hiddenimports=aubio_hiddenimports + [
        'aubio', 'librosa', 'soundfile', 'scipy', 'mutagen',
        'numpy', 'numpy._core', 'numpy._core._exceptions',
        'numpy._core.multiarray', 'numpy._core._multiarray_umath',
        'numpy._core._multiarray_tests', 'numpy._core.umath',
        'numpy._core._dtype_ctypes', 'numpy._core._methods',
        'numpy.lib.stride_tricks', 'numpy.fft', 'numpy.linalg',
        'scipy.signal', 'scipy.fft', 'scipy._lib.array_api_compat',
        'scipy._lib.array_api_compat.numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='R16_AudioTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='R16_AudioTool.app',
        icon=None,
        bundle_identifier='com.r16.audiotool',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '1.0.0',
        },
    )
