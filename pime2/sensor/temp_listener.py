# pylint: disable=consider-using-f-string
# pylint: disable=broad-except
import time
import board
import adafruit_dht
from pime2.log import pime_logger

#Set input pin for Sensor and set pulseio to False so that pin still can be used after shutdown of program
dhtDevice = adafruit_dht.DHT22(board.D12, use_pulseio=False)

#Start listening
try:
    while True:
        try:
            temp_c = dhtDevice.temperature
            if temp_c is not None:
                pime_logger.logging.info("Temp:{0:0.1f}°C".format(temp_c))
            else:
                pime_logger.logging.error("Failed to get reading. Try again!")
            time.sleep(2.0)
        except RuntimeError as error:
            pime_logger.logging.error(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            pime_logger.logging.exception('Exception occured, ending sensor listening')
            break
except KeyboardInterrupt:
    #Ending sensor listening with ctrl+c
    pime_logger.logging.info('Ending sensor listening')
