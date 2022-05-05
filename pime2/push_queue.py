# pylint: disable=global-statement, global-variable-not-assigned
import asyncio

# do not use this variable outside this class
RECEIVE_QUEUE: asyncio.Queue


def init_push_queue():
    """
    This (asyncio Queue init) has to be executed in main run() of asyncio

    :return:
    """
    global RECEIVE_QUEUE
    RECEIVE_QUEUE = asyncio.Queue()


def get_push_queue() -> asyncio.Queue:
    """
    Method to access receive queue

    :return:
    """
    return RECEIVE_QUEUE
