import asyncio
import logging

from typing import List
from zmq.asyncio import Context

import pime2.database as db
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
    connection = None
    try:
        connection = db.create_connection("pime_database.db")
        init_push_queue()
        zmq_context = Context.instance()

        enabled_sensors: List[Sensor] = [
           # ButtonSensor(DualPinOperatorArguments(12, 13, is_test_mode=True))
        ]
        # speaker = Speaker(SinglePinOperatorArguments(12, is_test_mode=True))

        # speaker.open()
        # speaker.activate(0.005)
        tasks = map(asyncio.create_task,
                    [startup_server(), startup_pull_queue(zmq_context),
                     startup_push_queue(zmq_context),
                     startup_sensor_listener(enabled_sensors)])
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        db.disconnect(connection)
        logging.info("ME2 application TERMINATED")
        