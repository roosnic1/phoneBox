from EmulatorGUI import GPIO
#import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
numCount = 0


def numBottonDown(channel):
    # if
    global numCount
    numCount += 1


def numPrint(channel):
    global numCount
    if numCount != 0:
        print(numCount)
        numCount = 0


GPIO.add_event_detect(23, GPIO.FALLING, callback=numBottonDown, bouncetime=80)
GPIO.add_event_detect(24, GPIO.FALLING, callback=numPrint, bouncetime=20)
