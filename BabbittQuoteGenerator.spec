# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('database', 'database'), ('config', 'config'), ('core', 'core'), ('gui', 'gui'), ('export', 'export'), ('utils', 'utils'), ('data', 'data')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 'docx', 'docx.shared', 'docx.enum.text', 'sqlite3', 'json', 'pathlib', 'datetime', 'tempfile', 'shutil', 'subprocess', 'sys', 'os', 're', 'typing', 'logging', 'colorama', 'pydantic'],
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
    name='BabbittQuoteGenerator',
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
