import RPi.GPIO as GPIO
from pime2.log import pime_logger
import time

#Initialising buttons on pins
button1 = 13
button2 = 14

#Initialising GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

isButtonOneUp = False
isButtonTwoUp = False

#Start listening
try:
    while True:
        if GPIO.input(button1) == GPIO.HIGH:
            pime_logger.logging.info("Knopf 1 unten")
            isButtonOneUp = False
            time.sleep(2.0)
        if GPIO.input(button1) == GPIO.LOW:
            pime_logger.logging.info("Knopf 1 oben")
            isButtonOneUp = True
            time.sleep(2.0)
        if GPIO.input(button2) == GPIO.LOW:
            pime_logger.logging.info("Knopf 2 oben")
            isButtonTwoUp = True
            time.sleep(2.0)
        if GPIO.input(button2) == GPIO.HIGH:
            pime_logger.logging.info("Knopf 2 unten")
            isButtonTwoUp = False
            time.sleep(2.0)
except KeyboardInterrupt:
    #Ending sensor listening with ctrl+c
    pime_logger.logging.info('Ending sensor listening')
    if isButtonOneUp == False:
        print('button one not up')