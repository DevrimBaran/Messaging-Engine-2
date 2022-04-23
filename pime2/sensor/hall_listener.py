from RPi import GPIO
import logging


# Start listening
async def is_magnetic():
    """
    Start sensor listening
    """
    # Set input Pin
    sensor = 18

    # Initialising GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor, GPIO.IN)
    if GPIO.input(sensor) == GPIO.HIGH:
        logging.info("No Magnetic field detected")
        magnet = False
    else:
        logging.info("Magnetic field detected")
        magnet = True
    return magnet
