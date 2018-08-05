import serial
import time

ser = serial.Serial("com3", 9600)

line = ser.readline()
print line[:-1]
print "-------"
ser.write("w 05 aaaaaaaaaaaabbbb")
time.sleep(3)
line = ser.read(ser.in_waiting)
print line[:-1]
print "-------"

ser.write("r 05")
time.sleep(1)
line = ser.read(ser.in_waiting)
print line[:-1]
print "-------"

ser.write("close")
time.sleep(1)
line = ser.read(ser.in_waiting)
print line[:-1]
print "-------"
