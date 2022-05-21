import socket
import time
import aiocoap

class NeighbourDiscovery():

    async def ip_scan(self):
        port = 5683
        result = []

        for x in range(1, 255):
            target = "192.168.178."
            target = target + str(x)
            t_IP = socket.gethostbyname(target)
            print ('Starting scan on host: ', t_IP)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.01)

            start = time.time()

            if self.port_scan(s, t_IP, port):
                print(f'port {port} is open')
                result.append(target)


            end = time.time()
            print(f'Time taken {end-start:.2f} seconds')

        print(result)

    def port_scan(self, socket, t_IP, port):
        try:
            socket.connect((t_IP, port))
            return True
        except:
            return False


    def send_hello(self):
        payload = "{ message: hello message }"
        #request = aiocoap.Message(code=aiocoap.Code.POST, payload=payload, uri=target)




