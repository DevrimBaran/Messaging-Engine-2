# pylint: disable=W1203
# pylint: disable=W0703
# pylint: disable=E1121
import logging
import time
import socket
from pime2.service.node_service import NodeService
from aiocoap import Code
from pime2.coap_client import ping, send_message


async def find_neighbours():
    """
    Finds all available hosts
    """
    available_ip = []

    for suffix in range(1, 255):
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

        logging.info("All neighbours found: %s", available_ip)

    await send_hello(available_ip)


def find_local_subnet():
    """
    Extracts the local subnet from the local ip of the host.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0)
    try:
        # doesn't even have to be reachable
        sock.connect(('8.8.8.8', 1))
        local_ip = sock.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        sock.close()
    local_subnet = ".".join(local_ip.split(".")[:-1]) + "."
    return local_subnet


async def send_hello(available_ip):
    """
    Sends a hello message to all its neighbours
    """
    service = NodeService()
    own_node = service.get_own_node()
    own_node_json = service.entity_to_json(own_node)
    for neighbour in available_ip:
        neighbour_response = await send_message(neighbour, "hello", own_node_json.encode() , Code.PUT)
        service.put_node(neighbour_response.payload.decode())
    return True

async def send_goodbye(all_neighbours):
    """
    Sends a goodbye message to all its neighbours
    """
    service = NodeService()
    own_node = service.get_own_node()

    # TODO: Get own node from NodeService end sent it to the neighbours. (Maybe only the node name)
    for neighbour in all_neighbours:
        await send_message(neighbour, "hello", b"hello neighbour", Code.PUT)
    return True
