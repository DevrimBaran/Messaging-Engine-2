import logging
import time
import pime2.coap_client as coap_client

async def find_neighbours():
    available_ip = []
    hello_messages = []

    for x in range(1, 80):
        try:
            target = "192.168.137."
            target = target + str(x)
            logging.info('Starting scan on host: %s', target)

            start = time.time()

            is_ping_successful = await coap_client.ping(target, returnPayload = True)
            if (is_ping_successful):
                available_ip.append(target)
                hello_messages.append(is_ping_successful)
            else:
                logging.info("No device on: %s", target)

        
        except Exception as exception:
            logging.error("Error while searching for neighbours: %s", exception)
        finally:
            end = time.time()
            logging.info(f'Time taken {end-start:.2f} seconds')

        end = time.time()
        logging.info(f'Time taken {end-start:.2f} seconds')

    print(available_ip)
    print(hello_messages)


def send_hello():
    payload = "{ message: hello message }"
    #request = aiocoap.Message(code=aiocoap.Code.POST, payload=payload, uri=target)




