import board
import adafruit_dht
import logging


async def return_temperature():
    """
    Start sensor listening
    """
    # Set input pin for Sensor and set pulseio to False so that pin still can be used after shutdown of program
    dhtDevice = adafruit_dht.DHT22(board.D12, use_pulseio=False)
    while True:
        try:
            temp_c = dhtDevice.temperature
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
