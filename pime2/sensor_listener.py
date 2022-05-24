import asyncio
import json
import logging
from typing import List

import pime2.config
from pime2.message import SensorResultMessage
from pime2.push_queue import get_push_queue
from pime2.sensor.sensor import Sensor


async def single_sensor_read(sensor: Sensor):
    """
    read sensor data and put it to the in-queue

    :param sensor:
    :return:
    """
    sensor_result = sensor.read()
    logging.info("Read sensor data: %s", sensor_result.__dict__)
    await get_push_queue().put(
        json.dumps(SensorResultMessage(sensor.sensor_type.value, sensor_result.__dict__).__dict__))


async def listen_sensor(sensor: Sensor):
    """
    # Run forever and (almost exactly) each second

    :param sensor:
    :return:
    """
    conf = pime2.config.get_me_conf()
    while True:
        await asyncio.gather(
            single_sensor_read(sensor),
            asyncio.sleep(conf.read_interval),
        )


async def startup_sensor_listener(sensors: List[Sensor]):
    """
    start asyncio tasks and wait for them to complete.
    Should be called in main asyncio run().

    :param sensors:
    :return:
    """

    # init sensors
    for sensor in sensors:
        sensor.open()

    task_list = []
    try:
        for sensor in sensors:
            task_list.append(asyncio.create_task(listen_sensor(sensor)))
        logging.info("Started %d sensor listening tasks", len(task_list))

        # normally wait forever here
        for task in task_list:
            await task
    finally:
        # close sensors "finally"
        for sensor in sensors:
            sensor.close()
