import serial
import serial.tools.list_ports
import time

arduino = serial.Serial("COM3", 9600)
data = []

time.sleep(2)
arduino.write(b'S,')


time.sleep(1)
arduino.write(b'255,1,1,')


time.sleep(1)
arduino.write(b'1,255,1,')
