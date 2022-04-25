import asyncio

# do not use this variable outside this class
receive_queue: asyncio.Queue


def init_push_queue():
    """
    This (asyncio Queue init) has to be executed in main run() of asyncio

    :return:
    """
    global receive_queue
    receive_queue = asyncio.Queue()


def get_push_queue() -> asyncio.Queue:
    """
    Method to access receive queue

    :return:
    """
    global receive_queue
    return receive_queue
