# pylint: disable=consider-using-f-string
import logging
import board
import adafruit_dht


async def return_temperature():
    """
    Start sensor listening
    """
    # Set input pin for Sensor and set pulseio to False so that pin still can be used after shutdown of program
    dht_device = adafruit_dht.DHT22(board.D12, use_pulseio=False)
    while True:
        try:
            temp_c = dht_device.temperature
            if temp_c is not None:
                logging.info("Temp:{0:0.1f}°C".format(temp_c))
                temperature = temp_c
                break
            logging.error("Failed to get reading. Try again!")
            continue
        except RuntimeError as error:
            logging.error(error.args[0])
            temperature = error.args[0]
            break
    return temperature
