import socketserver
import pickle
from dataclasses import dataclass
import sys


@dataclass
class Sensor:
    info = None
    name = None
    time = None


class TCPHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""

    def handle(self):
        sensor_data = (None, None, None)
        print("\nClient address: ", self.client_address)
        while True:
            messages = self.connection.recv(1024)
            msg_size = sys.getsizeof(messages)

            if messages == b'':
                print("\n\tClosing message received from: ", self.client_address)
                print("\tClosing message received: ", messages,
                      "\t\tMessage size: ", msg_size, type(messages))
                print("\t[ Done with messages from: ", sensor_data.name, " ]\n")
                break

            print("\nMessage received from: ", self.client_address,
                  "\tMessage size: ", msg_size, type(messages))
            sensor_data: Sensor() = pickle.loads(messages)
            print('Sensor() content: ', sensor_data.name,
                  '\t', sensor_data.info, '\t', sensor_data.time)


def main():
    """server"""
    host, port = 'localhost', 4000
    with socketserver.ThreadingTCPServer((host, port), TCPHandler) \
            as server:
        server.timeout = 300
        print('Sensor management listening on:', (host, port))
        server.serve_forever()


if __name__ == '__main__':
    main()
