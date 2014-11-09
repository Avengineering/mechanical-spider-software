import serial
import getopt, sys
import select

mySerial = serial.Serial('/dev/ttyACM0', 9600)

def getSerial():
    return mySerial.readline()

def checkStdin(callback):
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        data = sys.stdin.readline()
        if data == "exit":
            exit()
        callback(data)

def printOut(data):
    mySerial.write(data)


if __name__=="__main__":
    while True:
        checkStdin(printOut)
