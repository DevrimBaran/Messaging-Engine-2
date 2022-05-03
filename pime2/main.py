import asyncio
import logging

from typing import List
from zmq.asyncio import Context

from pime2.coap_server import startup_server
from pime2.push_queue import init_push_queue
from pime2.sensor.sensor import Sensor
from pime2.sensor_listener import startup_sensor_listener
from pime2.zmq import startup_pull_queue, startup_push_queue


async def pime_run():
    """
    main method of ME 2
    is executed in asyncio main run()

    :return:
    """
    logging.info("ME2 application STARTED")
    init_push_queue()
    zmq_context = Context.instance()

    enabled_sensors: List[Sensor] = [
        # ButtonSensor(OperatorArguments(12, is_test_mode=True))
    ]
    tasks = map(asyncio.create_task,
                [startup_server(), startup_pull_queue(zmq_context),
                 startup_push_queue(zmq_context),
                 startup_sensor_listener(enabled_sensors)])
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    logging.info("ME2 application TERMINATED")
