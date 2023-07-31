import datetime
import os
import pickle
import socketserver
import sqlite3
import sys
from dataclasses import dataclass
import psycopg2
from dotenv import load_dotenv


@dataclass
class Sensor:
    name: str = None
    measurement: int = 0
    taken_on: datetime = None
    '''
    Time the measurement was taken.
    '''


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
            print('Trying to save:', sensor_data)
            save(sensor_data)
            print('Sensor:', sensor_data, ' successfully saved')


def save(sensor: Sensor):
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="sensorhub-postgresql.c5jrbbbr7rhi.us-east-2.rds.amazonaws.com",
        port='5432'
    )
    print('Connected to', connection.host, connection.port)
    cursor = connection.cursor()

    query = "INSERT INTO sensors(name, taken_on, measurement) VALUES (?, ?, ?)"
    cursor.execute(query, (sensor.name, sensor.taken_on, sensor.measurement))
    connection.commit()

    rows = cursor.execute("SELECT name, taken_on, measurement FROM sensors").fetchall()
    connection.commit()
    cursor.close()
    print(rows)
    connection.close()


def load_schema(schema_file):
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="sensorhub-postgresql.c5jrbbbr7rhi.us-east-2.rds.amazonaws.com",
        port='5432'
    )
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
