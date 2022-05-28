# pylint: disable=W1203
# pylint: disable=W0703
# pylint: disable=E1121
import logging
import time
import socket
from aiocoap import Code
from pime2.coap_client import ping, send_message


async def find_neighbours(custom_subnet = None):
    """
    Finds all available hosts
    Note: In Windows you have to give the subnet as parameter into find_neighbours.
    Example: find_neighbours("192.168.30.")
    """
    available_ip = []

    for suffix in range(1, 256):
        if custom_subnet:
            subnet = custom_subnet
        else:
            subnet = find_local_subnet()

        target = subnet + str(suffix)

        logging.info('Starting scan on host: %s', target)

        start = time.time()
        try:
            is_ping_successful = await ping(target)
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


async def send_hello(available_ip):
    """
    Sends a hello message to all its neighbours
    """
    # TODO: Get all known neighbours from database
    # TODO: Get own node from nodeServide end send it to the neighbours
    for neighbour in available_ip:
        neighbour_response = await send_message(neighbour, "hello", b"hello neighbour", Code.PUT)
    return True

async def send_goodbye(all_neighbours):
    """
    Sends a goodbye message to all its neighbours
    """
    # TODO: Get own node from NodeService end sent it to the neighbours. (Maybe only the node name)
    for neighbour in all_neighbours:
        await send_message(neighbour, "hello", b"hello neighbour", Code.PUT)
    return True
