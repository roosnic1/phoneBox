#!/usr/bin/env python

import logging
import logging.handlers
import sys
import traceback
import time  # this is only being used as part of the example

from musicHandler import MusicHandler

from gpioHandler import GpioHandler

# Deafults
LOG_FILENAME = "./myservice.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger('phoneBox')
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and stderr in the log
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
# sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
# sys.stderr = MyLogger(logger, logging.ERROR)

def main():
    global music

    def gpioCallback(disc, track):
        return music.play(disc, track)

    def musicCallback(displayString):
        gpio.setDisplayTo(displayString)

    try:
        gpio = GpioHandler(gpioCallback)
        music = MusicHandler('./testData', musicCallback)
        print("Starting phoneBox")
        # Loop forever, doing something useful hopefully:
        i = 0
        while True:
            if not music.isSongPlaying() and gpio.isPowerOn():
                if music.isQueueEmpty():
                    music.play(0, 0)
                else:
                    music.next_song()
            if not gpio.isPowerOn():
                music.stop()
                gpio.switchDisplayOff()
            i += 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
        music.stop()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()
