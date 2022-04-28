import logging
import random

#from RPi import GPIO
from pime2.sensor.sensor import TwoPinSensor, SensorType, TwoPinSensorReadOutput, TwoPinOperatorArguments


class ButtonSensor(TwoPinSensor):
    def __init__(self, input_arguments: TwoPinOperatorArguments):
        super().__init__(SensorType.BUTTON, input_arguments)
        self.button_1 = input_arguments.input_pin_1
        self.button_2 = input_arguments.input_pin_2
        self.args = input_arguments

    def read(self) -> TwoPinSensorReadOutput:
        if self.args.is_test_mode is False:
            from RPi import GPIO
            # Start sensor listening
            if GPIO.input(self.button_1) == GPIO.HIGH:
                logging.info("Button 1 down")
                is_button_one_up = False
            if GPIO.input(self.button_1) == GPIO.LOW:
                logging.info("Button 1 up")
                is_button_one_up = True
            if GPIO.input(self.button_2) == GPIO.LOW:
                logging.info("Button 2 up")
                is_button_two_up = True
            if GPIO.input(self.button_2) == GPIO.HIGH:
                logging.info("Button 2 down")
                is_button_two_up = False
            return TwoPinSensorReadOutput(is_button_one_up, is_button_two_up)
        # Sensor dummy
        button_one_dummy = random.randint(0, 1)
        button_two_dummy = random.randint(0, 1)
        if button_one_dummy == 1:
            logging.info("Button 1 down")
            button_one_up = False
        else:
            logging.info("Button 1 up")
            button_one_up = True
        if button_two_dummy == 1:
            logging.info("Button 2 down")
            button_two_up = False
        else:
            logging.info("Button 2 up")
            button_two_up = True
        return TwoPinSensorReadOutput(button_one_up, button_two_up)

    def open(self):
        if self.args.is_test_mode is True:
            from RPi import GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def close(self):
        # Müsste GPIO.cleanup() auf pi testen um jegliche Fehler zu vermeiden. Funktioniert aber auch ohne.
        pass
