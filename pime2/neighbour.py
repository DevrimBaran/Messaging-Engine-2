# pylint: disable=W1203
# pylint: disable=W0703
import logging
import time
import socket
import pime2.coap_client as coap_client


async def find_neighbours(custom_subnet = None):
    """
    Finds all available hosts
    Note: In Windows you have to give the subnet as parameter into find_neighbours.
    Example: find_neighbours("192.168.30.")
    """
    available_ip = []

    for suffix in range(1, 255):
        if custom_subnet:
            subnet = custom_subnet
        else:
            subnet = find_local_subnet()

        target = subnet + str(suffix)

        logging.info('Starting scan on host: %s', target)

        start = time.time()
        try:
            is_ping_successful = await coap_client.ping(target)
            if is_ping_successful:
                available_ip.append(target)
            else:
                logging.info("No device on: %s", target)

        except Exception as exception:
            logging.error("Error while searching for neighbours: %s", exception)
        finally:
            end = time.time()
            logging.info(f'Time taken {end-start:.2f} seconds')

        end = time.time()
        logging.info(f'Time taken {end-start:.2f} seconds')

    return available_ip



def find_local_subnet():
    """
    Extracts the local subnet from the local ip of the host.
    Works not with Windows as expected.
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    local_subnet = ".".join(local_ip.split(".")[:-1])
    return local_subnet
