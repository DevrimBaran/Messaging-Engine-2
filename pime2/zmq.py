import zmq
from zmq.asyncio import Poller

from pime2.push_queue import get_push_queue


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
    print("Push queue started")
    poller = Poller()
    poller.register(socket, zmq.POLLOUT)

    receive_queue = get_push_queue()
    while True:
        result = await receive_queue.get()
        print(f"sent msg: {result}")
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
    print("Pull queue started")
    poller = Poller()
    poller.register(socket, zmq.POLLIN)

    while True:
        events = await poller.poll()
        if socket in dict(events):
            print("recving", events)
            msg = await socket.recv_multipart()
            print('recvd', msg)
