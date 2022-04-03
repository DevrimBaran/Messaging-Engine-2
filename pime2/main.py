import asyncio
import pime2.database as db

from zmq.asyncio import Context

from pime2.coap_server import startup_server
from pime2.demo import sender_task
from pime2.zmq import startup_pull_queue, startup_push_queue


async def pime_run():
    """
    main method of PIME2

    :return:
    """
    connection = db.create_connection("pime_database.db")
    zmq_context = Context.instance()
    send_queue = asyncio.Queue()
    tasks = map(asyncio.create_task,
                [startup_server(), startup_pull_queue(zmq_context), startup_push_queue(zmq_context, send_queue),
                 sender_task(send_queue)])
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    db.disconnect(connection)
