import json
import logging
import time
import ipaddress
from socket import socket, AF_INET, SOCK_STREAM, timeout
from aiocoap import Code
from pime2.service.node_service import NodeService
from pime2.config import get_me_conf
from pime2.coap_client import ping, send_message, coap_request_to_node
from pime2 import NEIGHBOR_DISCOVER_TIMEOUT


async def find_neighbors():
    """
    Finds all available hosts
    """
    port = get_me_conf().port
    available_ip = []

    ip_list = find_local_subnet()

    for target in ip_list:
        start = time.time()
        try:
            with socket(AF_INET, SOCK_STREAM) as s:
                s.settimeout(NEIGHBOR_DISCOVER_TIMEOUT)
                logging.info('Starting scan on host: %s', target)
                s.connect((target, port))

                available_ip.append(target)
                logging.info("Instance found!")
        except timeout:
            logging.info("No instance!")
        except Exception as exception:
            logging.error("Error while searching for neighbors: %s", exception)
        finally:
            end = time.time()
            logging.info("Time taken: %s seconds", round(end - start, 2))
    logging.info("All neighbors found: %s", available_ip)
    await send_hello(available_ip)


def find_local_subnet():
    """
    Extracts the local subnet from the ip of the host.
    """
    host_addr = get_me_conf().host
    ip = ipaddress.ip_address(host_addr)
    ip_list = []
    if isinstance(ip, ipaddress.IPv4Address):
        host_net = ipaddress.ip_network("%d.%d.%d.0/24" % (ip.packed[0], ip.packed[1], ip.packed[2]))
        ip_list = [str(ip) for ip in host_net][1:-1]
        return ip_list
    return ip_list


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
        logging.info("Sending hello to %s:5683", neighbor_ip)
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
        logging.info("Sending goodbye to: %s:%s", neighbor.name, neighbor.port)
        await coap_request_to_node(neighbor, "goodbye", own_node_json.encode(), Code.DELETE, timeout=1)
