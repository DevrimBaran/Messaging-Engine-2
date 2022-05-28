import asyncio

from pime2.config import get_me_conf


async def startup_silent_task():
    """
    Silent task to keep the application alive.
    Is called in main task execution and runs forever.
    Could be used as management or reporting task later.

    :param queue:
    :return:
    """
    while True:
        await asyncio.sleep(float(get_me_conf().read_interval))
