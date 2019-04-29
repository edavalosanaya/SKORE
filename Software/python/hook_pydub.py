import os
import sys
import pathlib

cwd = os.path.dirname(os.path.abspath(__file__))
if cwd == '' or cwd.find('SKORE') == -1:
        cwd = os.path.dirname(sys.argv[0])

bin_folder_location_1 = r".\dependencies\libav-x86_64-w64-mingw32-20160825\usr\bin"
bin_folder_location_2 = r".\libav-x86_64-w64-mingw32-20160825\usr\bin"

bin_folder_location_1_path = pathlib.Path(bin_folder_location_1)
bin_folder_location_2_path = pathlib.Path(bin_folder_location_2)

if bin_folder_location_1_path.is_dir():
    print("PYTHON IMPORT")
    os.environ["PATH"] += os.pathsep + bin_folder_location_1
elif bin_folder_location_2_path.is_dir():
    print("EXE IMPORT")
    os.environ["PATH"] += os.pathsep + bin_folder_location_2
else:
    print("Pydub import failure")
