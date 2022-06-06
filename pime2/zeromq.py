# pylint: disable=broad-except,no-member
import asyncio
import logging

import zmq
from zmq.asyncio import Poller

from pime2.flow import FlowManager, FlowValidationService, FlowOperationManager
from pime2.flow.flow_message_builder import FlowMessageBuilder
from pime2.router import router_loop
from pime2.push_queue import get_push_queue
from pime2.service.node_service import NodeService


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
    while True:
        result = await receive_queue.get()
        logging.info("sent msg: %s", result)
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
    flow_manager = FlowManager(FlowOperationManager(), FlowMessageBuilder(), NodeService())

    while True:
        try:
            events = await poller.poll()
            if socket in dict(events):
                msg = await socket.recv_multipart()
                try:
                    await asyncio.wait_for(router_loop(msg, flow_manager), timeout=60)
                except asyncio.exceptions.TimeoutError:
                    logging.warning("Message processing timeout reached!")
                except Exception as ex:
                    logging.error("Message processing inner exception: %s", ex)
        except Exception as e:
            logging.error("Message processing outer exception: %s", e)
        finally:
            logging.info("Message processing finished")
