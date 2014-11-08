import serial
import getopt, sys

mySerial = serial.Serial('/dev/ttyACM0', 9600)

def getdata():
    return mySerial.readline()

if __name__=="__main__":
    while 1:
        print mySerial.readline()
