
# MP3 -> WAV

#from pydub import AudioSegment
#from pydub.playback import play
#input_file = r'C:\Users\daval\Documents\GitHub\SKORE\Software\python\conversion_test\Original_MP3\OdeToJoy.mp3'
#sound = AudioSegment.from_mp3(input_file)
#output_file = r'C:\Users\daval\Documents\GitHub\SKORE\Software\python\temp\Original_MP3.wav'
#sound.export(output_file, format="wav")

# PDF -> XML

# gradle run -PcmdLineArgs="-batch,-export,-output,<my output folder>,--,<my file.pdf>"

# XML -> MIDI

#from music21 import *
#input_file_dir = r'C:\Users\daval\Documents\GitHub\SKORE\Software\python\conversion_test\audiverius_samples\SpiritedAway.mxl'
#input_file_dir = input_file_dir.replace('\\', '/')
#score = converter.parse(input_file_dir)
#score.write('midi','SpiritedAway.mid')

# MIDI (XML) -> PDF

# Use MuseScore instead
# cd <to the location of MuseScore.exe>
# MuseScore "<input file (xml or midi)>" -o "<output file (pdf) >"
