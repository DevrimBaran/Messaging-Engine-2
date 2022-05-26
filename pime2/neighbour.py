import logging
import time
import pime2.coap_client as coap_client

"""
Finds all available hosts
Note: In Windows you have to give the subnet as parameter into find_neighbours. Example: find_neighbours("192.168.30.")
"""
async def find_neighbours(custom_Subnet = None):
    available_ip = []

    for x in range(1, 255):
        try:
            if (custom_Subnet):
                subnet = custom_Subnet
            else:
                subnet = find_local_subnet()
            
            target = subnet + str(x)

            logging.info('Starting scan on host: %s', target)

            start = time.time()

            is_ping_successful = await coap_client.ping(target)
            if (is_ping_successful):
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


"""
Extracts the local subnet from the local ip of the host.
Works not with Windows as expected.
"""
def find_local_subnet():
    hostname = socket.gethostname()
    local_IP = socket.gethostbyname(hostname)
    local_subnet = ".".join(local_IP.split(".")[:-1])
    return local_subnet







