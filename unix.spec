# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None


a = Analysis(['src/main/python/main.py'],
             pathex=[os.path.dirname(os.path.realpath('__file__'))],
             binaries=[],
             datas=[("src/main/resources", "resources")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Pepys',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False ,
          icon='src/main/resource/appicons/pepys-icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Pepys')
