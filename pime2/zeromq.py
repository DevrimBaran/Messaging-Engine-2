# pylint: disable=no-member
import asyncio
import logging

import zmq
from zmq.asyncio import Poller

from pime2 import ROUTER_LOOP_TASK_TIMEOUT
from pime2.config import get_me_conf
from pime2.flow.flow_manager import FlowManager
from pime2.router import router_loop
from pime2.push_queue import get_push_queue
from pime2.service.node_service import NodeService
from pime2.database import get_db_connection
from pime2.repository.queue_repository import QueueRepository


async def startup_push_queue(context):
    """
    Starting a push queue of ZMQ and waits for sender_queue events to push messages to the zmq socket.
    Runs forever.

    :param context:
    :return:
    """
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5555")
    logging.info("Push queue started")
    poller = Poller()
    poller.register(socket, zmq.POLLOUT)

    receive_queue = get_push_queue()
    queue_repository = QueueRepository(get_db_connection())
    old_queue = queue_repository.get_all_from_push_queue()
    for msg in old_queue:
        await receive_queue.put(msg, True)
    while True:
        result = await receive_queue.get()
        
        logging.debug("sent msg: %s", result)
        await socket.send_multipart([str(result).encode('ascii')])
        receive_queue.task_done()


async def startup_pull_queue(context):
    """
    Starting a pull queue of ZMQ and waiting for receive events.
    Runs forever.

    :param context:
    :return:
    """
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:5555")
    logging.info("Pull queue started")
    poller = Poller()
    poller.register(socket, zmq.POLLIN)

    # load and instantiate flow manager
    flow_manager = FlowManager(NodeService())
    conf = get_me_conf()

    while True:
        try:
            events = await poller.poll()
            if socket in dict(events):
                msg = await socket.recv_multipart()
                try:
                    await asyncio.wait_for(router_loop(msg, flow_manager), timeout=ROUTER_LOOP_TASK_TIMEOUT)
                except asyncio.exceptions.TimeoutError:
                    logging.warning("Message processing timeout reached!")
                except Exception as ex:
                    logging.error("Message processing inner exception: %s", ex)
                    if conf.is_debug:
                        raise RuntimeError("Problem executing ME2") from ex
        except Exception as e:
            logging.error("Message processing exception: %s", e)
            if conf.is_debug:
                raise RuntimeError("Problem during execution of ME2") from e
        finally:
            logging.debug("A single router loop has finished")
