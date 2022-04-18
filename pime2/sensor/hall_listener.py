import RPi.GPIO as GPIO
from pime2.log import pime_logger
import time

#Set input Pin
sensor = 18

#Initialising GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN)

#Start listening
try:
    while True:
        if (GPIO.input(sensor) == GPIO.HIGH):
            pime_logger.logging.info("No Magnetic field detected")
            time.sleep(2.0)
        else:
            pime_logger.logging.info("Magnetic field detected")
            time.sleep(2.0)
except KeyboardInterrupt:
    #Ending sensor listening with ctrl+c
    pime_logger.logging.info('Ending sensor listening')