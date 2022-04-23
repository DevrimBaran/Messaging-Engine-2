import random
import logging


def temperature_dummy():
    """
    Temp sensor dummy
    """
    random_temperature = random.randint(-50, 50)
    logging.info("Temp: " + str(random_temperature))
    return random_temperature
