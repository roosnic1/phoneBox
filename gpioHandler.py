import RPi.GPIO as GPIO

class GpioHandler(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # GPIO.setup(25, GPIO.IN)
        self.numCount = 0
        GPIO.add_event_detect(24, GPIO.FALLING, callback=self.wheelFinishedCallback, bouncetime=20)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.numberPassesCallback, bouncetime=80)


    def numberPassesCallback(self, channel):
        self.numCount += 1

    def wheelFinishedCallback(self, channel):
        print(self.numCount)
        self.numCount = 0