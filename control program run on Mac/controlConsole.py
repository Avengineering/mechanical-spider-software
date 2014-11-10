import sys
import select
import time
import serial

bluetooth = serial.Serial('/dev/tty.HC-06-DevB',9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.1)

def checkBluetooth(callback):
    bluetoothData = bluetooth.readline()
    if bluetoothData:
        callback(bluetoothData)

def checkStdin(callback):
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        data = sys.stdin.readline()
        if data:
            callback(data)
    return

def writeData(data):
    bluetooth.write(data)
    return

def writeToConsole(data):
    sys.stdout.write(data)
    return

def console_main():
    while True:
        checkStdin(writeData)
        checkBluetooth(writeToConsole)

if __name__=="__main__":
    console_main()