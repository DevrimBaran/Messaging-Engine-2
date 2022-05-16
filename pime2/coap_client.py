import asyncio
from wsgiref.util import request_uri
import aiocoap
from aiocoap import Message, Context
import logging

class CoapClient:

    def __init__(self):
        self.client_context = Context.create_client_context()
        logging.info("Created Client")

    async def ping(self, destination):
        logging.info("Sending Ping request")
        code=aiocoap.Code.POST
        uri='coap://' + destination + '/trigger-hello'
        request = Message(code=code, uri=uri)
        logging.debug("Request:" + "\tcode= " + request.code + "\turi= " + uri )
        try:
            response = await self.client_context.request(request).response
            logging.debug("Response: " + response)
        except Exception as exception:
            logging.error('Ping failed! Exception: ' + exception)
        else:
            logging.info(' Ping succesful! Response: %s\n%r' % (response.code, response.payload))

    async def send_message(self, destination, endpoint, payload):
        logging.info("Sending Message request")
        code=aiocoap.Code.POST
        uri='coap://' + destination + '/' + endpoint
        request = Message(code=code, uri=uri, payload=payload)
        logging.debug("Request: payload= " + payload + "\tcode= " + code + "\turi= " + uri )
        try:
            response = await self.client_context.request(request).response
            logging.debug("Response: " + response)
        except Exception as exception:
            logging.error('Sending Message failed! Exception: ' + exception)
        else:
            logging.info('Message Request succesful: %s\n%r' % (response.code, response.payload))