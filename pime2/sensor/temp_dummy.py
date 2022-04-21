import random
from pime2.log import pime2_logger


def temp_dummy():
    """
    Temp sensor dummy
    """
    random_temp = random.randint(-50, 50)
    pime2_logger.logging.info("Temp: " + str(random_temp))
    return random_temp
