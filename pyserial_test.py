import serial
import time

ser = serial.Serial("/dev/cu.usbmodem145131")

line = ser.readline()
print line[:-1]
print "-------"
ser.write("python received!")
time.sleep(1)
line = ser.read(ser.in_waiting)
print line[:-1]
print "-------"