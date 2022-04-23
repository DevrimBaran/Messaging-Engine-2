import logging


def vibration_dummy(var_on):
    """
    vibration dummy
    """
    if var_on == 1:
        pime2_logger().info("Vibration motor is on")
        return True
    return False
