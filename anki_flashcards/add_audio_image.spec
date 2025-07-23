# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['add_audio_image.py'],
    pathex=["C:\\Users\\lovek\\PycharmProjects\\ForFun\\anki_flashcards"],
    binaries=[],
    datas=[],
    hiddenimports=["check_duplication","reformat_word_list"],
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
    name='add_audio_image',
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
    icon=['ico\\anki_flashcards.ico'],
)
