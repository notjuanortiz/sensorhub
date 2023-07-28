import datetime
import socketserver
import pickle
from dataclasses import dataclass
import sys

@dataclass
class Sensor:
    info = 0
    name = "name"
    time = None

class exeTCPHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""

    def handle(self):
        print ("\nClient address: ", self.client_address,\
                "\nConnection details: ", self.connection, )
        while True: 
            messages = self.connection.recv(1024)
            #serverTimestamp = datetime.datetime.now()

            pkSize = sys.getsizeof(messages)
            if (pkSize > 50): print("\nSize of received message: ", pkSize, type(messages))
            else: print("\n\tClosing message size: ", pkSize, type(messages))

            if messages == b'' :
                print("\t[ Done with messages from: ", sensor_data.name, " ]\n")
                break

            sensor_data: Sensor() = pickle.loads(messages)
            print('Sensor() content: ', sensor_data.name,\
                  '\t', sensor_data.info, '\t', sensor_data.time)
            
def main():
    # server
    host, port = 'localhost', 4000
    with socketserver.ThreadingTCPServer((host, port), exeTCPHandler)\
    as server:
        server.timeout = 300
        print('Sensor management listening on:', (host, port))
        server.serve_forever()

if __name__ == '__main__':
    main()