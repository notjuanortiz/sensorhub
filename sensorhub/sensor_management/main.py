import csv
import os
import pickle
import socketserver
import sqlite3
import sys
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Sensor:
    measurement: float = 0.0
    location: str = None
    timestamp: str = None


class SensorDataRequestHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""
    buffer_size = 2048

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


def write(data, filename: str):
    if not os.path.exists(filename):
        open(filename, 'w', newline='')

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(data)


def save(sensor: Sensor):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    query = "INSERT INTO sensors(measurement, location) VALUES (?, ?)"
    cursor.execute(query, (sensor.measurement, sensor.location))
    connection.commit()

    rows = cursor.execute("SELECT id, measurement, location FROM sensors").fetchall()
    print(rows)
    cursor.close()
    connection.close()


def load_schema(schema_file):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    with open(schema_file, "r") as file:
        schema = file.read()
    cursor.executescript(schema)
    connection.commit()
    cursor.close()
    connection.close()


def main():
    schema_file = 'schema.sql'
    load_schema(schema_file)
    load_dotenv()
    host: str = os.environ.get('TCP_HOST')
    port: int = int(os.environ.get('TCP_PORT'))
    with socketserver.ThreadingTCPServer((host, port), SensorDataRequestHandler) as server:
        print('Sensor management listening on:', (host, port))
        server.serve_forever()


if __name__ == '__main__':
    main()
