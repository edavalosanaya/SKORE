# -*- mode: python -*-

# Solving a recursion issue
import sys
sys.setrecursionlimit(5000)

# Placing a time stamp
import time
timestr = time.strftime("Y%YM%mD%d-H%HM%MS%S")

# Moving the platform folder of PyQt5 within the skore folder.
import shutil
exe_path = 'C:\\Users\\daval\\Documents\\GitHub\\SKORE\\Software\\python'
exe_name = 'skore' + '-' + timestr

block_cipher = None

added_files = [
        ('config.yml', '.'),
        ('.\\images', 'images'),
        ('.\\misc', 'misc'),
        ('.\\conversion_test', 'conversion_test'),
        ('.\\dependencies\\opencv_ffmpeg344_64.dll', '.'),
        ('.\\dependencies\\api-ms-win-downlevel-shlwapi-l1-1-0.dll', '.'),
        ('.\\dependencies\\libav-x86_64-w64-mingw32-20160825', 'libav-x86_64-w64-mingw32-20160825')
]

a = Analysis(['skore.py'],
             pathex=[exe_path],
             binaries=[],
             datas= added_files,
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
          name=exe_name,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True,
          icon = '.\\images\skore_icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name=exe_name)


# This is post file compilation
exe_folder = exe_path + '\\dist\\' + exe_name
src = exe_folder + '\\PyQt5\\Qt\\plugins\\platforms'
dst = exe_folder
shutil.move(src, dst)
