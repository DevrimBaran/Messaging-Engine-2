# pylint: disable=W1203
# pylint: disable=W0703
import logging
import time
import socket
from pime2.coap_client import ping


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

    return available_ip


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
