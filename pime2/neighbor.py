import json
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
            logging.info("Time taken: %s seconds", round(end - start, 2))

    logging.info("All neighbors found: %s", available_ip)

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
    Sends a hello message to all its neighbor.
    The message response contains the node of the neighbor, which then is saved in the database.
    After that it sends the own node to the neighbor
    """
    service = NodeService()
    own_node = service.get_own_node()
    own_node_json = service.entity_to_json(own_node)
    for neighbor_ip in available_ip:
        logging.info("Sending hello to %s", neighbor_ip)
        neighbor_response = await send_message(neighbor_ip, "hello", "Hello, I'm online!".encode(), Code.GET)
        neighbor_entity = service.json_to_entity(neighbor_response.payload.decode())
        service.put_node(neighbor_entity)
        await send_message(neighbor_ip, "nodes", own_node_json.encode(), Code.PUT)


async def send_goodbye():
    """
    Sends a goodbye message to all its neighbor
    """
    service = NodeService()
    own_node = service.get_own_node()
    own_node_json = json.dumps(own_node.__dict__)
    all_neighbors = service.get_all_neighbor_nodes()
    for neighbor in all_neighbors:
        logging.info("Sending goodbye to: %s ", neighbor.name)
        await send_message(neighbor.ip, "goodbye", own_node_json.encode(), Code.DELETE, timeout=1)
