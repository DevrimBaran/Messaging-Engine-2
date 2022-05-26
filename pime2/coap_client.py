# pylint: disable=W0703
# pylint: disable=W0611
import asyncio
import logging
from aiocoap import Code, Context, Message, numbers

TIMEOUT = 0.5

# workaround for timeout
# TODO: globals()["numbers"].REQUEST_TIMEOUT = 1.0
# globals()["numbers"].MAX_RETRANSMIT = 0

async def ping(destination):
    """
    Ping Implementation
    """
    logging.info("Created Client Context")
    client_context = await Context.create_client_context()
    logging.info("Sending Ping request")
    code = Code.GET
    uri = 'coap://' + destination + '/trigger-hello'
    request = Message(code=code, uri=uri)
    logging.debug("Request: code= %s \turi=  %s", code, uri)
    try:
        response = await asyncio.wait_for(client_context.request(request).response, timeout=TIMEOUT)
        logging.debug("Response: %s", response)
    except Exception as exception:
        logging.error('Ping failed! Exception: %s', exception)
        return False
    else:
        logging.info('Ping succesful! Response: %s\n%r', response.code, response.payload)
        return True


async def send_message(destination, endpoint, payload):
    """
    Send message with an arbitrary payload to a specific destination and endpoint.
    """
    logging.info("Created Client Context")
    client_context = Context.create_client_context()
    logging.info("Sending Message request")
    code = Code.POST
    uri = 'coap://' + destination + '/' + endpoint
    request = Message(code=code, uri=uri, payload=payload)
    logging.debug("Request: payload= %s \tcode= %s \turi=  %s", payload, code, uri)
    try:
        response = await client_context.request(request).response
        logging.debug("Response: %s", response)
    except Exception as exception:
        logging.error('Sending Message failed! Exception: %s', exception)
    else:
        logging.info('Message Request succesful: %s\n%r', response.code, response.payload)
