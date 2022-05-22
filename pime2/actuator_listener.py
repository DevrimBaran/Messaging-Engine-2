import asyncio
import json
import logging
from typing import List

from pime2.message import SensorResultMessage
from pime2.push_queue import get_push_queue
from pime2.actuator.actuator import Ac

async def single_actuator_read(actuator: Ac):
    """
    read sensor data and put it to the in-queue

    :param sensor:
    :return:
    """
    sensor_result = sensor.read()
    logging.info("Read sensor data: %s", sensor_result.__dict__)
    await get_push_queue().put(
        json.dumps(SensorResultMessage(sensor.sensor_type.value, sensor_result.__dict__).__dict__))