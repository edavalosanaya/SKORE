from pydub import AudioSegment
from pydub.playback import play
input_file = r'C:\Users\daval\Documents\GitHub\SKORE\python\conversion_test\Original_MP3\OdeToJoy.mp3'
sound = AudioSegment.from_mp3(input_file)
output_file = r'C:\Users\daval\Documents\GitHub\SKORE\python\temp\Original_MP3.wav'
sound.export(output_file, format="wav")
