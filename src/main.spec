# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('function', 'function'), ('icon', 'icon')],
    hiddenimports=['diff_match_patch'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='myShortcut',
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
    uac_admin=True,
    icon='./logo.ico',
)

import shutil

shutil.copyfile('./setting.ini', '{0}/setting.ini'.format(DISTPATH))
shutil.copyfile('./properties.ini', '{0}/properties.ini'.format(DISTPATH))
shutil.copyfile('./logo.ico', '{0}/logo.ico'.format(DISTPATH))
