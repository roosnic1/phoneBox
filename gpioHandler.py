import RPi.GPIO as GPIO
import time
import threading
from array import array
from Adafruit_LED_Backpack import SevenSegment
from Adafruit_LED_Backpack import HT16K33


""" Constants
    Pin 23: number count
    Pin 24: dail action 
"""
NUMBER_PIN = 23
DAIL_PIN = 24
POWER_PIN = 25


class GpioHandler(object):

    def __init__(self, numberCallback):
        """ Init of GPIO Pin
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NUMBER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(DAIL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(POWER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(NUMBER_PIN, GPIO.FALLING, callback=self.numberPassesCallback, bouncetime=80)
        GPIO.add_event_detect(DAIL_PIN, GPIO.BOTH, callback=self.dailCallback, bouncetime=20)
        # Var init
        self.numberCallback = numberCallback
        self.numberIter = 0
        self.numberDisplay = ['','','','']
        self.numberDisplayOld = ['','','','']
        self.lookFlag = False

        # Timer initialization
        self.t = threading.Timer(10.0, self.timeoutTimmer)

        # Create display instance on default I2C address (0x70) and bus number and clear Display
        self.display = SevenSegment.SevenSegment()
        self.display.begin()
        self.display.print_number_str('    ')
        self.display.write_display()
        self.display.clear()

        # Test Blinking function
        self.dispDrive = HT16K33.HT16K33()
        self.dispDrive.begin()

    def numberPassesCallback(self, channel):
        if self.numberDisplay[self.numberIter] == '-':
            self.numberDisplay.remove('-')
            self.numberDisplay.append(0)
        self.numberDisplay[self.numberIter] += 1
        if self.numberDisplay[self.numberIter] == 10:
            self.numberDisplay[self.numberIter] = 0
        self.displayRefresher()


    def dailCallback(self, Channel):
        time.sleep(0.02)
        if GPIO.input(DAIL_PIN):
            if len(self.numberDisplay) > 0 and self.numberIter == 0:
                self.numberDisplayOld = list(self.numberDisplay)
                self.numberDisplay = []
                self.lookFlag = True
            self.numberDisplay.append('-')
            self.displayRefresher()
            print('Timer status:', self.t.isAlive())
            if self.t and self.t.isAlive():
                self.t.cancel()
        else:
            self.numberIter += 1
            if self.numberIter >= 4:
                discID = ''.join(str(x) for x in self.numberDisplay[:2])
                songID = ''.join(str(x) for x in self.numberDisplay[2:])
                songExists = self.numberCallback(int(discID), int(songID))
                print('currentSong', songExists)
                self.dispDrive.set_blink(HT16K33.HT16K33_BLINK_2HZ)
                if not songExists:
                    for i,val in enumerate(self.numberDisplay):
                        self.numberDisplay[i] = '-'
                    self.displayRefresher()
                time.sleep(2)
                self.dispDrive.set_blink(HT16K33.HT16K33_BLINK_OFF)
                self.numberDisplay = list(self.numberDisplayOld)
                self.displayRefresher()
                self.numberIter = 0
                self.numberDisplay = ['','','','']
                self.lookFlag = False
            else:
                if self.t:
                    self.t = threading.Timer(10.0, self.timeoutTimmer)
                self.t.start()


    def timeoutTimmer(self):
        print('timeout :(')
        self.numberDisplay = list(self.numberDisplayOld)
        self.displayRefresher()
        self.numberIter = 0
        self.numberDisplay = ['', '', '', '']
        self.lookFlag = False

    def setDisplayTo(self, displayString):
            if self.lookFlag == False:
                for i, val in enumerate(displayString):
                    self.numberDisplay[i] = val
                self.displayRefresher()
            else:
                for i, val in enumerate(displayString):
                    self.numberDisplayOld[i] = val


    def displayRefresher(self):
        self.display.clear()
        self.display.print_number_str(''.join(str(x) for x in self.numberDisplay), False)
        self.display.write_display()

    def isPowerOn(self):
        return not GPIO.input(POWER_PIN)

    def switchDisplayOff(self):
        self.display.print_number_str('    ')
        self.display.write_display()
        self.display.clear()

