"""
Entry point of the PIME2 application
"""
import logging
import asyncio
import sys
from asyncio import WindowsSelectorEventLoopPolicy

from pime2.main import pime_run

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    handlers=[
                        logging.FileHandler("me2.log"),
                        logging.StreamHandler(sys.stdout)])
logging.getLogger("coap-server").setLevel(logging.DEBUG)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(pime_run())
