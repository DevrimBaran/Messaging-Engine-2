import logging


def vibration_dummy(var_on):
    """
    vibration dummy
    """
    if var_on == 1:
        logging.info("Vibration motor is on")
        return True
    return False
