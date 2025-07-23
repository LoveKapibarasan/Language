# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_dynamic_libs

binaries = collect_dynamic_libs("azure.cognitiveservices.speech")


a = Analysis(
    ['main.py'],
    pathex=["C:/Users/lovek/PycharmProjects/ForFun/azure_sounds"],
    binaries=binaries,
    datas=[],
    hiddenimports=["speech_to_text","text_to_speech"],
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
    name='azure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['ico\\azure.ico'],
)
