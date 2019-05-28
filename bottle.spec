# -*- mode: python -*-

# If locations.db is missing, run 'python db.py' to create a dummy dataset.

block_cipher = None

a = Analysis(['app_bottle.py'],
             pathex=[],
             binaries=[],
             datas=[('locations.db','.'), ('static/*','./static'), ('static/img/*','./static/img')],
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
          name='app_bottle',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='app_bottle')
