from skore_program_controller import *
clean_temp_folder()

input_a = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\Original_MP3\SpiritedAway.mp3"
input_b = temp_folder_path
auto_audacity(input_a,input_b)

input_c = temp_folder_path + '\\' + 'SpiritedAway.wav'
amazing_midi_test_input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\misc\piano0.wav"
auto_amazing_midi(input_c, input_b, amazing_midi_test_input)
