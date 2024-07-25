# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\joand\\PycharmProjects\\AutomTest\\assets', 'assets'),
        ('C:\\Users\\joand\\PycharmProjects\\AutomTest\\environment', 'environment'),
        ('C:\\Users\\joand\\PycharmProjects\\AutomTest\\dependencies', 'dependencies'),
    ],
    hiddenimports=['flask_cors', 'openai', 'google.generativeai', 'unidecode', 'spacy', 'pt_core_news_md'],
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
    name='app',
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
)
