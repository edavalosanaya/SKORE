#import os
#https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python
#https://stackoverflow.com/questions/17057544/python-extract-folder-path-from-file-path

import ntpath
import pathlib
import os

user_input_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\Original_MP3\SpiritedAway.mp3"
destination_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp"

#Getting the name of the file
filename = ntpath.basename(user_input_address)
print(filename)
filename2 = filename.split(".")[0]
print(filename2)

#Getting the path of the file
exist_path = pathlib.Path(user_input_address)
file_path = exist_path.parent
print(file_path)

#Getting the path of the original wav file
wav_input_address = str(file_path) + '\\' + filename2 + '.wav'
print(wav_input_address)
#Getting the end_address
end_address = destination_address + '\\' + filename2 + '.wav'
print(end_address)

#moving the file
#os.rename(user_input_address, end_address)
