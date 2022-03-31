import asyncio


async def sender_task(queue: asyncio.Queue):
    """
    Demo sender task to simulate some "traffic"

    :param queue:
    :return:
    """
    while True:
        await asyncio.sleep(2)
        queue.put_nowait("payload!")
