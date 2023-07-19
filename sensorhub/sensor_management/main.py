import csv
import datetime
import json
import os
import socketserver
from dataclasses import dataclass


@dataclass
class SensorData:
    sample_str: str
    sample_int: int
    sample_float: float


class ExampleTCPHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""

    def handle(self):
        messages = self.rfile.readlines()
        rawJson = ""
        for message in messages:
            message_fragment = message.decode('utf-8')
            rawJson += message_fragment

        incoming_data: SensorData = json.loads(rawJson)
        timestamp = datetime.datetime.now()
        print('Message received:', incoming_data)
        write([timestamp, incoming_data], 'sensor_logs.csv')


def write(data, filename: str):
    if not os.path.exists(filename):
        open(filename, 'w', newline='')

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(data)


def main():
    # server
    host, port = 'localhost', 4000
    with socketserver.ThreadingTCPServer((host, port), ExampleTCPHandler) as server:
        print('Sensor management listening on:', (host, port))
        server.serve_forever()


if __name__ == '__main__':
    main()
