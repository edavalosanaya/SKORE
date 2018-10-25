import serial
import serial.tools.list_ports
import time

arduino = serial.Serial("COM3", 9600)

while(True):
    time.sleep(2)
    message = ' '
    arduino.write(message.encode('utf-8'))
    print(".", end = '')
