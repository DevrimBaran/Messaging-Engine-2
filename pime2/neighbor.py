# pylint: disable=broad-except
import logging
import time
import socket
from aiocoap import Code
from pime2.service.node_service import NodeService
from pime2.config import get_me_conf
from pime2.coap_client import ping, send_message



async def find_neighbors():
    """
    Finds all available hosts
    """
    available_ip = []

    subnet = find_local_subnet()
    for suffix in range(1, 255):
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
            logging.error("Error while searching for neighbors: %s", exception)
        finally:
            end = time.time()
            logging.info("Time taken: %s seconds", round(end-start,2))

        end = time.time()
        logging.info("All neighbors found: %s", available_ip)

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
        sock.connect(('129.69.5.3', 80))
        local_ip = sock.getsockname()[0]
    except Exception:
        local_ip = get_me_conf().host
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
