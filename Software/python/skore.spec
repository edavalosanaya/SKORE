# -*- mode: python -*-

import sys

sys.setrecursionlimit(5000)

block_cipher = None

added_files = [
        ('config.yml', '.'),
        ('.\\images', 'images'),
        ('.\\misc', 'misc'),
        ('.\\temp', 'temp'),
        ('.\\templates', 'templates')
]


a = Analysis(['skore.py'],
             pathex=['C:\\Users\\daval\\Documents\\GitHub\\SKORE\\Software\\python'],
             binaries=[],
             datas= added_files,
             hiddenimports=['cv2'],
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
          name='skore',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon = '.\\images\skore_icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='skore')
