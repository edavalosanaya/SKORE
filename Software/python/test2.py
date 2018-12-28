import rtmidi
import serial
import serial.tools.list_ports
import time

from skore_lib import FileContainer, GuiManipulator, setting_read, setting_write, is_mid, rect_to_int

midi_in = rtmidi.MidiIn()
in_avaliable_ports = midi_in.get_ports()
selected_port = setting_read("piano_port")
midi_in.open_port(in_avaliable_ports.index(selected_port))

midi_out = rtmidi.MidiOut()
out_avaliable_ports = midi_out.get_ports()
midi_out.open_port(out_avaliable_ports.index("LoopBe Internal MIDI 1"))

while True:
    time.sleep(0.05)
    message = midi_in.get_message()

    if message:
        print(message)
        note_info, delay = message

        midi_out.send_message(message)
