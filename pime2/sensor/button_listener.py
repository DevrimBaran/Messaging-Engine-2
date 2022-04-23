from RPi import GPIO
import logging


async def return_button_listening():
    """
    Start sensor listening
    """
    # Initialising buttons on pins
    button1 = 13
    button2 = 14

    # Initialising GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    if GPIO.input(button1) == GPIO.HIGH:
        logging.info("Button 1 down")
        is_button_one_up = False
    if GPIO.input(button1) == GPIO.LOW:
        logging.info("Button 1 up")
        is_button_one_up = True
    if GPIO.input(button2) == GPIO.LOW:
        logging.info("Button 2 up")
        is_button_two_up = True
    if GPIO.input(button2) == GPIO.HIGH:
        logging.info("Button 2 down")
        is_button_two_up = False
    button_listening = is_button_one_up, is_button_two_up
    return button_listening
