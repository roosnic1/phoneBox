import RPi.GPIO as GPIO
import time
from array import array
from Adafruit_LED_Backpack.SevenSegment import SevenSegment

class GpioHandler(object):

    def __init__(self, numberCallback):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.numCount = 0
        self.numberCallback = numberCallback
        #self.numberDisplay = array('I', [0, 0, 0, 0])
        self.numberIter = 0
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.numberPassesCallback, bouncetime=80)
        GPIO.add_event_detect(24, GPIO.BOTH, callback=self.wheelCallback, bouncetime=20)
        #GPIO.add_event_detect(24, GPIO.RISING, callback=self.wheelStartedCallback, bouncetime=20)
        #GPIO.add_event_detect(24, GPIO.FALLING, callback=self.wheelFinishedCallback, bouncetime=20)

        # Create display instance on default I2C address (0x70) and bus number.
        self.display = SevenSegment.SevenSegment()
        self.display.begin()
        self.display.clear()


    def numberPassesCallback(self, channel):
        self.numberDisplay[self.numberIter] += 1
        if self.numberDisplay[self.numberIter] == 10:
            self.numberDisplay[self.numberIter] = 0
        self.displayRefresher()

    def wheelCallback(self, Channel):
        time.sleep(0.02)
        if GPIO.input(24):
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

    # def wheelStartedCallback(self, Channel):
    #     if self.numberIter == 0:
    #         self.numberDisplay = array('I', [0, 0, 0, 0])
    #     self.displayRefresher()
    #
    #
    # def wheelFinishedCallback(self, channel):
    #     self.numberIter += 1
    #     if self.numberIter >= 4:
    #         discID = ''.join(str(x) for x in self.numberDisplay[:2])
    #         songID = ''.join(str(x) for x in self.numberDisplay[2:])
    #         currentSong = self.numberCallback(discID, songID)
    #         if not currentSong[0]:
    #             for i,val in enumerate(self.numberDisplay):
    #                 self.numberDisplay[i] = '-'
    #             self.displayRefresher()
    #         for i, val in enumerate(currentSong[1]):
    #             self.numberDisplay[i] = val
    #         time.sleep(1)
    #         self.displayRefresher()
    #         self.numberIter = 0


    def displayRefresher(self):
        self.display.clear()
        self.display.print_number_str(''.join(str(x) for x in self.numberDisplay))
        self.display.write_display()
