"""
Entry point of the ME2 application
"""
import logging
import asyncio
import sys

from me2.config import load_app_config, CONFIG_FILE
from me2.main import me_run

if __name__ == "__main__":
    if sys.platform == "win32":
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    config = load_app_config(CONFIG_FILE)

    # configure logging
    logging.basicConfig(
        format='%(asctime)s - instance:' + config.instance_id + ' - %(name)s - %(levelname)s - %(message)s',
        level=config.loglevel,
        handlers=[
            logging.FileHandler("me2.log"),
            logging.StreamHandler(sys.stdout)])
    logging.getLogger("coap-server").setLevel(config.loglevel)
    logging.info("Loaded app's configuration from '%s' successfully", CONFIG_FILE)

    # start application
    try:
        asyncio.run(me_run(config))
    except Exception:
        logging.error("ME2 exited.")
