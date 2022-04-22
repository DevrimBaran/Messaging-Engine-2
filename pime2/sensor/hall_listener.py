# pylint: disable-all
from RPi import GPIO
from pime2.log.pime2_logger import pime2_logger

# Set input Pin
SENSOR = 18

# Initialising GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR, GPIO.IN)


# Start listening
async def return_is_magnetic():
    """
    Start sensor listening
    """
    try:
        while True:
            if GPIO.input(SENSOR) == GPIO.HIGH:
                pime2_logger().info("No Magnetic field detected")
                magnet = False
                break
            else:
                pime2_logger().info("Magnetic field detected")
                magnet = True
                break
    except KeyboardInterrupt:
        # Ending sensor listening with ctrl+c
        pime2_logger().info('Ending sensor listening')
    return magnet
