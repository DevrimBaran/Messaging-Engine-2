# pylint: disable=W0703
import logging
import aiocoap
from aiocoap import Message, Context

class CoapClient():
    """
    Coap Client Implementation
    """

    def __init__(self,client_context):
        """
        Initialize Coap Client.
        """
        self.client_context = client_context
        logging.info("Created Client")


    async def ping(self, destination):
        """
        Ping Implementation
        """
        logging.info("Sending Ping request")
        code = aiocoap.Code.GET
        uri = 'coap://' + destination + '/trigger-hello'
        request = Message(code=code, uri=uri)
        logging.debug("Request: code= %s \turi=  %s", code, uri)
        try:
            response = await self.client_context.request(request).response
            logging.debug("Response: %s", response)
        except Exception as exception:
            logging.error('Ping failed! Exception: %s', exception)
        else:
            logging.info('Ping succesful! Response: %s\n%r', response.code, response.payload)


    async def send_message(self, destination, endpoint, payload):
        """
        Send message with an arbitrary payload to a specific destination and endpoint.
        """
        logging.info("Sending Message request")
        code = aiocoap.Code.POST
        uri = 'coap://' + destination + '/' + endpoint
        request = Message(code=code, uri=uri, payload=payload)
        logging.debug("Request: payload= %s \tcode= %s \turi=  %s", payload, code, uri)
        try:
            response = await self.client_context.request(request).response
            logging.debug("Response: %s", response)
        except Exception as exception:
            logging.error('Sending Message failed! Exception: %s', exception)
        else:
            logging.info('Message Request succesful: %s\n%r', response.code, response.payload)
