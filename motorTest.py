import RPi.GPIO as GPIO
import sys
import select
import time
import Queue

LmotorPulsePin = 18
LmotorDirPin = 2
RmotorPulsePin = 23
RmotorDirPin = 24
sleepPin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(LmotorPulsePin, GPIO.OUT)
GPIO.setup(LmotorDirPin, GPIO.OUT)
GPIO.setup(RmotorPulsePin, GPIO.OUT)
GPIO.setup(RmotorDirPin, GPIO.OUT)
GPIO.setup(sleepPin, GPIO.OUT)

Lpwm = GPIO.PWM(LmotorPulsePin, 10)
Rpwm = GPIO.PWM(RmotorPulsePin, 10)

startTime = time.time()
jobQueue = Queue.Queue()

minTimeInterval = 0.015

array = (1175, 1319, 1046, 880, 880, 980, 784, 784, 587, 660, 523, 440, 440, 494, 392, 392\
         , 294, 330, 262, 220, 220, 247, 220, 208, 196, 196, 10, 10, 784, 784, 294, 311, \
         330, 523, 523, 330, 523, 523, 330, 523, 523, 523, 523, 523, 10, 1046, 1175, 1245,\
         1319, 1046, 1175, 1319, 1319, 988, 1175, 1175, 1046, 1046, 1046, 1046, 1046, 1046, 294, 311\
         , 330, 523, 523, 330, 523, 523, 330, 523, 523, 523, 523, 523, 10, 10, 880, 784, \
         740, 880, 1046, 1319, 1319, 1175, 1046, 880, 1175, 1175, 1175, 1175, 1175, 1175, 294, 311,\
         330, 523, 523, 330, 523, 523, 330, 523, 523, 523, 523, 523, 10, 1046, 1175, 1245,\
         1319, 1046, 1175, 1319, 1319, 988, 1175, 1175, 1046, 1046, 1046, 1046, 1046, 10, 1046, 1175,\
         1319, 1046, 1175, 1319, 1319, 1046, 1175, 1046, 1319, 1046, 1175, 1319, 1319, 1046, 1175, 1046,\
         1319, 1046, 1175, 1319, 1319, 988, 1175, 1175, 1046, 1046, 1046, 1046, 1046, 1046, 294, 311, \
         330, 523, 523, 330, 523, 523, 330, 523, 523, 523, 523, 523, 10, 1046, 1175, 1245,\
         1319, 1046, 1175, 1319, 1319, 988, 1175, 1175, 1046, 1046, 1046, 1046, 1046, 1046, 294, 311\
         , 330, 523, 523, 330, 523, 523, 330, 523, 523, 523, 523, 523, 10, 10, 880, 784, \
         740, 880, 1046, 1319, 1319, 1175, 1046, 880, 1175, 1175, 1175, 1175, 1175, 1175, 294, 311,\
         330, 523, 523, 330, 523, 523, 330, 523, 523, 523, 523, 523, 10, 1046, 1175, 1245,\
         1319, 1046, 1175, 1319, 1319, 988, 1175, 1175, 1046, 1046, 1046, 1046, 1046, 10, 1046, 1175,\
         1319, 1046, 1175, 1319, 1319, 1046, 1175, 1046, 1319, 1046, 1175, 1319, 1319, 1046, 1175, 1046,\
         1319, 1046, 1175, 1319, 1319, 988, 1175, 1175, 1046, 1046, 1046, 1046, 1046, 1046)
def checkStdin():
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        data = sys.stdin.readline()
        if data:
            if data == "exit\n":
                GPIO.cleanup()
                exit()
            if data == "s\n":
                Lpwm.stop()
                Rpwm.stop()
            if data == "play\n":
                Lpwm.start(1)
                Rpwm.start(1)
                GPIO.output(sleepPin, GPIO.HIGH)
                for i in array:
                    Lpwm.ChangeFrequency(i)
                    Rpwm.ChangeFrequency(i)
                    time.sleep(0.2)
                Lpwm.stop()
                Rpwm.stop()
            if data == "sl\n":
                Lpwm.stop()
                Rpwm.stop()
                GPIO.output(sleepPin, GPIO.LOW)
            if "," in data:
                endTime = time.time()
                global startTime
                if endTime-startTime>=minTimeInterval:
                    if not jobQueue.empty():
                        jobQueue.put(data)
                        data = jobQueue.get()
                    startTime = endTime
                    executeCommand(data)
                else:
                    jobQueue.put(data)

def executeCommand(data):
    splitData = data.split(",")
    LmotorSpeed = 100*int(splitData[0])
    RmotorSpeed = 100*int(splitData[1])
                
    Lpwm.start(1)
    Rpwm.start(1)
    GPIO.output(sleepPin, GPIO.HIGH)
    if LmotorSpeed >= 0:
        if LmotorSpeed==0:
            Lpwm.stop()
        else:
            GPIO.output(LmotorDirPin, GPIO.LOW)
            Lpwm.ChangeFrequency(LmotorSpeed)
    else:
        GPIO.output(LmotorDirPin, GPIO.HIGH)
        Lpwm.ChangeFrequency(-LmotorSpeed)
    if RmotorSpeed >=0:
        if RmotorSpeed==0:
            Rpwm.stop()
        else:
            GPIO.output(RmotorDirPin, GPIO.HIGH)
            Rpwm.ChangeFrequency(RmotorSpeed)
    else:
        GPIO.output(RmotorDirPin, GPIO.LOW)
        Rpwm.ChangeFrequency(-RmotorSpeed)

def checkJob():
    global startTime
    endTime = time.time()
    if not jobQueue.empty() and endTime-startTime>=minTimeInterval:
        startTime = endTime
        data = jobQueue.get()
        executeCommand(data)




if __name__=="__main__":
    while True:
        checkStdin()
        checkJob()