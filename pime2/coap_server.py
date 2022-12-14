import asyncio
import logging

import aiocoap
from aiocoap import resource

import pime2.config
from pime2.res.default import Default
from pime2.res.flow import Flow
from pime2.res.goodbye import Goodbye
from pime2.res.flow_message import FlowMessage
from pime2.res.health import Health
from pime2.res.hello import Hello
from pime2.res.node import Node
from pime2.res.operation import Operation


async def startup_server():
    """
    Starting the CoAp server and running it forever

    :return:
    """
    root = resource.Site()

    # Expose CoAp endpoint info
    root.add_resource(['.well-known', 'core'],
                      resource.WKCResource(root.get_resources_as_linkheader))

    root.add_resource(['flows'], Flow())
    root.add_resource(['flow-messages'], FlowMessage())
    root.add_resource(['hello'], Hello())
    root.add_resource(['goodbye'], Goodbye())
    root.add_resource(['health'], Health())
    root.add_resource(['nodes'], Node())
    root.add_resource(['operations'], Operation())
    root.add_resource([''], Default())

    conf = pime2.config.get_me_conf()
    await aiocoap.Context.create_server_context(bind=(conf.host, conf.port), site=root)

    logging.info("Started CoAp-Server at %s:%s", conf.host, conf.port)
    # Run forever
    await asyncio.get_running_loop().create_future()
