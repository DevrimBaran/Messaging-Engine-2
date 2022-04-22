from RPi import GPIO
from pime2.log.pime2_logger import pime2_logger

# Initialising buttons on pins
BUTTON1 = 13
BUTTON2 = 14

# Initialising GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


async def return_button_listening():
    """
    Start sensor listening
    """
    try:
        while True:
            if GPIO.input(BUTTON1) == GPIO.HIGH:
                pime2_logger().info("Button 1 down")
                is_button_one_up = False
            if GPIO.input(BUTTON1) == GPIO.LOW:
                pime2_logger().info("Button 1 up")
                is_button_one_up = True
            if GPIO.input(BUTTON2) == GPIO.LOW:
                pime2_logger().info("Button 2 up")
                is_button_two_up = True
            if GPIO.input(BUTTON2) == GPIO.HIGH:
                pime2_logger().info("Button 2 down")
                is_button_two_up = False
            break
    except KeyboardInterrupt:
        # Ending sensor listening with ctrl+c
        pime2_logger().info('Ending sensor listening')
        if is_button_one_up is False:
            print('button one not up')
    button_listening = is_button_one_up, is_button_two_up
    return button_listening
