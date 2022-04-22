import random
from pime2.log.pime2_logger import pime2_logger


def temp_dummy():
    """
    Temp sensor dummy
    """
    random_temp = random.randint(-50, 50)
    pime2_logger().info("Temp: " + str(random_temp))
    return random_temp
