import asyncio
import logging
from aiocoap import Code, Context, Message

# workaround for timeout
# TODO: globals()["numbers"].REQUEST_TIMEOUT = 1.0
# globals()["numbers"].MAX_RETRANSMIT = 0
from pime2 import NEIGHBOR_DISCOVER_PING_TIMEOUT


async def ping(destination):
    """
    Ping Implementation
    takes an IP as destination and sends a get request to its hello endpoint
    """
    client_context = await Context.create_client_context()
    logging.info("Sending Ping request")
    code = Code.GET
    uri = 'coap://' + destination + '/hello'
    request = Message(code=code, uri=uri)
    logging.debug("Request: code= %s \turi=  %s", code, uri)
    try:
        response = await asyncio.wait_for(client_context.request(request).response,
                                          timeout=NEIGHBOR_DISCOVER_PING_TIMEOUT)
        logging.debug("Response: %s", response)
    except Exception as exception:
        logging.error('Ping failed! Exception: %s', exception)
        return False
    else:
        logging.info('Ping successful! Response: %s\n%r', response.code, response.payload)
        return True


async def send_message(destination, endpoint, payload, code, timeout=30):
    """
    Send message with an arbitrary payload to a specific destination and endpoint.
    Takes an IP as destination, an endpoint of the destination and the payload to send
    """
    client_context = await Context.create_client_context()
    logging.info("Sending Message request")
    uri = 'coap://' + destination + '/' + endpoint
    request = Message(code=code, uri=uri, payload=bytes(str(payload).encode("utf-8")))
    logging.debug("Request: payload= %s \tcode= %s \turi=  %s", payload, code, uri)
    try:
        response = await asyncio.wait_for(client_context.request(request).response,
                                                timeout=timeout)
        logging.debug("Response: %s", response)
    except Exception as ex:
        logging.error('Sending Message to %s/%s failed! Exception: %s', destination, endpoint, ex)
        return False
    else:
        logging.info('Message Request successful: %s\n%r', response.code, response.payload)
        return response or True
