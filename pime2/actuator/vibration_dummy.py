from pime2.log.pime2_logger import pime2_logger


def vibration_dummy(var_on):
    """
    vibration dummy
    """
    if var_on == 1:
        pime2_logger().info("Vibration motor is on")
        return True
    return False
