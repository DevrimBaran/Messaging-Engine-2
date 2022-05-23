import json
import logging

import zmq
from zmq.asyncio import Poller

from pime2.message import MessageType
from pime2.push_queue import get_push_queue
from pime2.sensor.sensor import SensorType


async def startup_push_queue(context):
    """
    Starting a push queue of ZMQ and waits for sender_queue events to push messages to the zmq socket.
    Runs forever.

    :param context:
    :return:
    """
    # pylint: disable=E1101
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
    # pylint: disable=E1101
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:5555")
    logging.info("Pull queue started")
    poller = Poller()
    poller.register(socket, zmq.POLLIN)

    while True:
        events = await poller.poll()
        if socket in dict(events):
            msg = await socket.recv_multipart()
            received_object = json.loads(msg[0])
            if "message_type" in received_object and received_object["message_type"] is not None:
                message_type = received_object["message_type"]
                if message_type == MessageType.SENSOR_RESULT.value:
                    logging.debug("detected sensor_read for sensor %s", SensorType(received_object["sensor_type"]))
                elif message_type == MessageType.NODE_CREATE.value:
                    # TODO store node entry in database
                    logging.debug("detected node create event with node: %s")
                logging.info("received message json: %s", received_object)
            else:
                logging.error("problem with received message: %s", received_object)

        # TODO: implement message processing engine here
