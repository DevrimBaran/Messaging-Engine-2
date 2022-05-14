"""
Entry point of the PIME2 application
"""
import logging
import asyncio
import sys

from pime2.config import load_app_config, CONFIG_FILE
from pime2.main import pime_run

if __name__ == "__main__":
    if sys.platform == "win32":
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    config = load_app_config(CONFIG_FILE)

    # configure logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=config.loglevel,
                        handlers=[
                            logging.FileHandler("me2.log"),
                            logging.StreamHandler(sys.stdout)])
    logging.getLogger("coap-server").setLevel(config.loglevel)
    logging.info("Loaded app's configuration from '%s' successfully", CONFIG_FILE)

    # start application
    asyncio.run(pime_run(config))
