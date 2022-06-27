# pylint: disable=global-statement, global-variable-not-assigned
import asyncio
from pime2.database import get_db_connection
from pime2.repository.queue_repository import QueueRepository

class PersistentQueue(asyncio.Queue):
    async def put(self, item, startup = False):
        if (not startup):
            queue_repository = QueueRepository(get_db_connection())
            queue_repository.put_into_push_queue(item)
        return await super().put(item)
    
    async def get(self):
        queue_repository = QueueRepository(get_db_connection())
        queue_repository.pull_from_push_queue()
        return await super().get()

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


