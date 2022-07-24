# pylint: disable=global-statement, global-variable-not-assigned
import asyncio
from pime2.database import get_db_connection
from pime2.repository.queue_repository import QueueRepository

class PersistentQueue(asyncio.Queue):
    """Overrides the put and get methods of the queue to make it persistent"""
    def __init__(self):
        super().__init__()
        self.queue_repository = QueueRepository(get_db_connection())

    def put_nowait(self, item, startup = False):
        if not startup:
            self.queue_repository.put_into_push_queue(item)
        return super().put_nowait(item)

    def put(self, item):
        self.queue_repository.put_into_push_queue(item)
        return super().put(item)


# do not use this variable outside this class
RECEIVE_QUEUE: PersistentQueue

def init_push_queue():
    """
    This (asyncio Queue init) has to be executed in main run() of asyncio

    :return:
    """
    global RECEIVE_QUEUE
    RECEIVE_QUEUE = PersistentQueue()


def get_push_queue() -> PersistentQueue:
    """
    Method to access receive queue

    :return:
    """
    return RECEIVE_QUEUE
