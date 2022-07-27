import asyncio
import json
import logging
import time
import ipaddress
from aiocoap import Code
from pime2.service.node_service import NodeService
from pime2.config import get_me_conf
from pime2.coap_client import send_message, coap_request_to_node, ping


async def find_neighbors():
    """
    Finds all available hosts
    """
    task_list = []

    ip_list = find_local_subnet()

    start = time.time()
    for target in ip_list:
        try:
            task_list.append(asyncio.create_task(run_ping(target)))
            # wait a short time, before firing another request
            await asyncio.sleep(0.05)
        except Exception as exception:
            logging.error("Error while searching for neighbors: %s", exception)

    success_ip_list = []
    for task in task_list:
        result, ip = await task
        if result:
            success_ip_list.append(ip)

    logging.info("%s neighbors found: %s. Took %s seconds", len(success_ip_list), success_ip_list,
                 round(time.time() - start, 2))
    await send_hello(success_ip_list)


def find_local_subnet():
    """
    Extracts the local subnet from the ip of the host.
    """
    host_addr = get_me_conf().host
    ip = ipaddress.ip_address(host_addr)
    ip_list = []
    if isinstance(ip, ipaddress.IPv4Address) and not ip.is_global:
        # pylint: disable=consider-using-f-string
        host_net = ipaddress.ip_network("%d.%d.%d.0/24" % (ip.packed[0], ip.packed[1], ip.packed[2]))
        ip_list = [str(ip) for ip in host_net][1:-1]
        return ip_list
    return ip_list


async def run_ping(target) -> (bool, str):
    """Run ping"""
    return await ping(target), target


async def send_hello(available_ip):
    """
    Sends a hello message to all its neighbor.
    The message response contains the node of the neighbor, which then is saved in the database.
    After that it sends the own node to the neighbor
    """
    service = NodeService()
    own_node = service.get_own_node()
    own_node_json = service.entity_to_json(own_node)
    for neighbor in available_ip:
        ip_address = str(neighbor)

        logging.info("Sending hello to %s:5683", ip_address)
        neighbor_response = await send_message(ip_address, "hello", "Hello, I'm online!".encode(), Code.GET)
        if neighbor_response is False:
            logging.error("Problem receiving node from ip %s", ip_address)
            return
        neighbor_entity = service.json_to_entity(neighbor_response.payload.decode())
        service.put_node(neighbor_entity)
        await send_message(ip_address, "nodes", own_node_json.encode(), Code.PUT)


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


def cleanUpAllNodes():
    """
    Removes all known neighbors and recreates own node
    """
    service = NodeService()
    service.delete_all_nodes()
    service.create_own_node()
    logging.info("Cleaned all neighbors and recreated own node.")
    
