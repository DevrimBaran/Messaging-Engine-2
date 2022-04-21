# pylint: disable=consider-using-f-string
# pylint: disable=broad-except
# pylint: no-else-break
import board
import adafruit_dht
from pime2.log import pime2_logger

# Set input pin for Sensor and set pulseio to False so that pin still can be used after shutdown of program
dhtDevice = adafruit_dht.DHT22(board.D12, use_pulseio=False)


# Start listening
async def return_temp():
    """
    Start sensor listening
    """
    try:
        while True:
            try:
                temp_c = dhtDevice.temperature
                if temp_c is not None:
                    pime2_logger.logging.info("Temp:{0:0.1f}°C".format(temp_c))
                    temperature = temp_c
                    break
                else:
                    pime2_logger.logging.error("Failed to get reading. Try again!")
                    continue
            except RuntimeError as error:
                pime2_logger.logging.error(error.args[0])
                temperature = error.args[0]
                break
    except KeyboardInterrupt:
        # Ending sensor listening with ctrl+c
        pime2_logger.logging.info('Ending sensor listening')
    return temperature
