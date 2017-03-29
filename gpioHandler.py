import RPi.GPIO as GPIO
import time
from array import array
from Adafruit_LED_Backpack import SevenSegment
from Adafruit_LED_Backpack import HT16K33


NUMBER_PIN          = 23
DAIL_PIN           = 24


class GpioHandler(object):

    def __init__(self, numberCallback):
        """Init of GPIO Pin
        Pin 24: dail action 
        Pin 25: number count"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NUMBER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(DAIL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(NUMBER_PIN, GPIO.FALLING, callback=self.numberPassesCallback, bouncetime=80)
        GPIO.add_event_detect(DAIL_PIN, GPIO.BOTH, callback=self.dailCallback, bouncetime=20)

        # Var init
        self.numCount = 0
        self.numberCallback = numberCallback
        self.numberIter = 0

        # Create display instance on default I2C address (0x70) and bus number and clear Display
        self.display = SevenSegment.SevenSegment()
        self.display.begin()
        self.display.print_number_str('1234')
        self.display.write_display()
        self.display.clear()

        # Test Blinking function

        self.dispDrive = HT16K33.HT16K33()
        self.dispDrive.begin()
        self.dispDrive.set_blink('HT16K33_BLINK_HALFHZ')
        time.sleep(2)


    def numberPassesCallback(self, channel):
        self.numberDisplay[self.numberIter] += 1
        if self.numberDisplay[self.numberIter] == 10:
            self.numberDisplay[self.numberIter] = 0
        self.displayRefresher()


    def dailCallback(self, Channel):
        time.sleep(0.02)
        if GPIO.input(DAIL_PIN):
            if self.numberIter == 0:
                self.numberDisplay = array('I', [0, 0, 0, 0])
            self.displayRefresher()
        else:
            self.numberIter += 1
            if self.numberIter >= 4:
                discID = ''.join(str(x) for x in self.numberDisplay[:2])
                songID = ''.join(str(x) for x in self.numberDisplay[2:])
                currentSong = self.numberCallback(discID, songID)
                if not currentSong[0]:
                    for i,val in enumerate(self.numberDisplay):
                        self.numberDisplay[i] = '-'
                    self.displayRefresher()
                for i, val in enumerate(currentSong[1]):
                    self.numberDisplay[i] = val
                time.sleep(1)
                self.displayRefresher()
                self.numberIter = 0


    def displayRefresher(self):
        self.display.clear()
        self.display.print_number_str(''.join(str(x) for x in self.numberDisplay))
        self.display.write_display()
