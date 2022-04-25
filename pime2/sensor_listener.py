import asyncio
import logging
from typing import List

from pime2.main import get_receive_queue
from pime2.types.sensor import Sensor


async def single_sensor_read(sensor: Sensor):
    """
    read sensor data and put it to the in-queue

    :param sensor:
    :return:
    """
    sensor_result = sensor.read()
    logging.info(f"Read sensor data: {str(sensor_result)}")
    # TODO: define object to exchange here
    await get_receive_queue().put({f"sensor_result: {str(sensor_result)}"})


async def listen_sensor(sensor: Sensor):
    """
    # Run forever and (almost exactly) each second

    :param sensor:
    :return:
    """
    while True:
        await asyncio.gather(
            single_sensor_read(sensor),
            asyncio.sleep(1.0),
        )


async def sensor_listener(sensors: List[Sensor]):
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
        logging.info(f"Started {len(task_list)} sensor listening tasks")

        # normally wait forever here
        for task in task_list:
            await task
    finally:
        # close sensors "finally"
        for sensor in sensors:
            sensor.close()
