import datetime
import socketserver
import pickle
from dataclasses import dataclass
import sys
#from dataclasses import dataclass

@dataclass
class Sensor:
    info = 0
    name = "name"

class exeTCPHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""

    def handle(self):
        while True: 
            messages = self.connection.recv(300)
            pkSize = sys.getsizeof(messages)
            if (pkSize > 50): print("size of message\t-\t", pkSize)
            else: print("\t\tClosing message size\t-\t", pkSize)
            #messages = self.rfile.readlines()

            #raw_byte_string  = b''  
            #for message in messages:
            #    raw_byte_string += message

            #if raw_byte_string == b'' : break
            if messages == b'' : break
            #sensor_data: Sensor() = pickle.loads(raw_byte_string)
            #sensor_data: Sensor() = pickle.loads(messages[0])
            sensor_data: Sensor() = pickle.loads(messages)
            timestamp = datetime.datetime.now()
            print('Message received:', sensor_data)
            print('sensorDATA:\t', sensor_data.name ,'\t', sensor_data.info)
            #print('Message received:', messages[0])
        print("\n\t[ Done with messages from:\t", sensor_data.name, " ]\n")
            

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
