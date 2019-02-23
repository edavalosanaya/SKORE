from lib_skore import read_config
import os

cfg = read_config()

mus_app_exe_path = cfg['app_path']['muse_score']
mus_app_exe_directory = os.path.dirname(mus_app_exe_path)
mus_app_exe_filename = os.path.basename(mus_app_exe_path)

mp3_file = r"C:\Users\daval\Documents\GitHub\SKORE\Software\python\conversion_test\mp3_samples\SpiritedAway.mp3"
wav_file = r"C:\Users\daval\Documents\GitHub\SKORE\Software\python\temp\OdeToJoy.wav"

os.system('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mp3_file, wav_file))
