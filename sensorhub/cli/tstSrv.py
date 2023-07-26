import datetime
import socketserver
import pickle
from dataclasses import dataclass
#from dataclasses import dataclass

@dataclass
class Sensor:
    info = 0
    name = "name"

class exeTCPHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""

    def handle(self):
        messages = self.rfile.readlines()
        raw_byte_string  = b''  
        for message in messages:
            raw_byte_string += message

        sensor_data: Sensor(0) = pickle.loads(raw_byte_string)
        timestamp = datetime.datetime.now()
        print('Message received:', sensor_data)
        print('sensorDATA:\t', sensor_data.name ,'\t', sensor_data.info)
        #print('Message received:', messages[0])


def main():
    # server
    host, port = 'localhost', 4000
    with socketserver.ThreadingTCPServer((host, port), exeTCPHandler)\
    as server:
        print('Sensor management listening on:', (host, port))
        server.serve_forever()


if __name__ == '__main__':
    main()
