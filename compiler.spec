# -*- mode: python ; coding: utf-8 -*-

import os
from dotenv import load_dotenv
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Charger les variables d'environnement
load_dotenv()
python_package_path = os.getenv("PYTHON_PACKAGE_PATH")


a = Analysis(
    ['timer_app\\main.py'],
    pathex=["./timer_app"],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'scipy',
        # 'IPython', 'notebook', 'nbconvert', 'nbformat', 'docutils', 'zmq',  'parso', 'jedi', 'lxml.isoschematron', 'bcrypt', 'cryptography', 'gevent', 'PyQt5', 'cffi'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QuevOfTimeApp',
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

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QuevOfTimeApp',
)
