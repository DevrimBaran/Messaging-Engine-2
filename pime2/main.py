import asyncio

from typing import List
from zmq.asyncio import Context

from pime2.coap_server import startup_server
from pime2.receive_queue import get_receive_queue, init_receive_queue
from pime2.sensor_listener import sensor_listener
from pime2.types.sensor import Sensor
from pime2.zmq import startup_pull_queue, startup_push_queue


async def pime_run():
    """
    main method of PIME2

    :return:
    """
    init_receive_queue()
    zmq_context = Context.instance()

    enabled_sensors: List[Sensor] = [
        # ButtonSensor(OperatorArguments(12, is_test_mode=True))
    ]
    tasks = map(asyncio.create_task,
                [startup_server(), startup_pull_queue(zmq_context),
                 startup_push_queue(zmq_context, get_receive_queue()),
                 sensor_listener(enabled_sensors)])
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
