# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\\main\\python\\main.py'],
             pathex=['C:\\Users\\lukeb\\Documents\\Projects\\Pepys'],
             binaries=[],
             datas=[("src/main/resources", "resources")],
             hiddenimports=["enchant.tokenize.en"],
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
          name='pepys',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon=r'src/main/resources/base/icons/appicons/pepys-icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               console=False,
               name='pepys')
