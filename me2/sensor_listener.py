import asyncio
import json
import logging

import me2.config
from me2.actuator.actuator_manager import ActuatorManager
from me2.config import get_me_conf
from me2.message import SensorResultMessage
from me2.push_queue import get_push_queue
from me2.sensor.sensor import Sensor


async def single_sensor_read(sensor: Sensor):
    """
    read sensor data and put it to the in-queue

    :param sensor:
    :return:
    """
    sensor_result = sensor.read()
    logging.info("Read sensor data: %s", sensor_result.__dict__)
    get_push_queue().put_nowait(
        json.dumps(SensorResultMessage(sensor.sensor_type.value, sensor_result.__dict__).__dict__))


async def listen_sensor(sensor: Sensor):
    """
    # Run forever and (almost exactly) each second

    :param sensor:
    :return:
    """
    conf = me2.config.get_me_conf()
    while True:
        await asyncio.gather(
            single_sensor_read(sensor),
            asyncio.sleep(conf.read_interval),
        )


async def startup_operator_listener():
    """
    start asyncio tasks and wait for them to complete.
    Should be called in main asyncio run().
    Runs forever.

    :param sensors:
    :return:
    """
    # load actuators
    conf = get_me_conf()
    am = ActuatorManager()
    for actuator in conf.available_actuators:
        am.open(actuator.actuator_type)

    # init sensors
    sensors = conf.available_sensors
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

    if len(task_list) == 0:
        # Just run forever if there are no sensors
        await asyncio.get_running_loop().create_future()
