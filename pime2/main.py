import asyncio
import logging

from typing import List
from zmq.asyncio import Context

import pime2.database as db
import pime2.neighbour as Neighbour
from pime2.coap_server import startup_server
from pime2.common.operator import DualPinOperatorArguments
from pime2.push_queue import init_push_queue
from pime2.sensor.button_sensor import ButtonSensor
from pime2.sensor.sensor import Sensor
from pime2.sensor_listener import startup_sensor_listener
from pime2.zmq import startup_pull_queue, startup_push_queue
import pime2.coap_client
from aiocoap import Context as ctx


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
        client = pime2.coap_client.CoapClient(await ctx.create_client_context())
        enabled_sensors: List[Sensor] = [
            ButtonSensor(DualPinOperatorArguments(12, 13, is_test_mode=True))
        ]
        await client.ping(destination="192.168.137.58")
        tasks = map(asyncio.create_task,
                    [startup_server(), startup_pull_queue(zmq_context),
                     startup_push_queue(zmq_context),
                     startup_sensor_listener(enabled_sensors)])

        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


    finally:
        db.disconnect(connection)
        logging.info("ME2 application TERMINATED")