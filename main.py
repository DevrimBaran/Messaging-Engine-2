"""
Entry point of the PIME2 application
"""
import logging
import asyncio

from pime2.main import pime_run

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(pime_run())
