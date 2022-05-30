import asyncio
import logging
import sys

from zmq.asyncio import Context

import pime2.database as db
from pime2.neighbor import find_neighbors
from pime2.coap_server import startup_server
from pime2.config import MEConfiguration
from pime2.database import create_default_tables
from pime2.push_queue import init_push_queue
from pime2.sensor_listener import startup_sensor_listener
from pime2.silent import startup_silent_task
from pime2.zmq import startup_pull_queue, startup_push_queue


async def pime_run(config: MEConfiguration):
    """
    main method of ME 2
    is executed in asyncio main run()

    :param config MEConfiguration
    :return:
    """
    logging.info("ME2 application STARTED")
    connection = None
    try:
        connection = db.create_connection("pime_database.db")
        init_push_queue()
        create_default_tables(connection)
        zmq_context = Context.instance()

        try:
            enabled_sensors = config.available_sensors()
        except RuntimeError as config_error:
            logging.error("Problem with sensor configuration: '%s'", config_error)
            sys.exit(1)

        if config.is_neighbor_discovery_enabled:
            await find_neighbors()

        tasks = map(asyncio.create_task,
                    [startup_server(), startup_pull_queue(zmq_context),
                     startup_push_queue(zmq_context),
                     startup_sensor_listener(enabled_sensors),
                     startup_silent_task()])
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        db.disconnect(connection)
        logging.info("ME2 application TERMINATED")
