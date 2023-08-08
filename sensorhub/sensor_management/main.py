import os
import pickle
import socketserver
import sys
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from sensor import Sensor, SensorService
from storage_connectors import PostgreSQLConnector

service = SensorService()


class SensorDataRequestHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""
    buffer_size = 2048

    def handle(self):
        sensor = (None, None, None)
        print("\nClient address: ", self.client_address)
        while True:
            messages = self.connection.recv(self.buffer_size)
            msg_size = sys.getsizeof(messages)

            if messages == b'':
                print("\n\tClosing connection from: ", self.client_address)
                break

            print("\nMessage received from: ", self.client_address)

            sensor: Sensor = pickle.loads(messages)

            # deserialize sensor (matches clients data structure)
            sensor.measurement = sensor.info
            sensor.taken_on = sensor.time
            print("Found:", sensor)
            service.save(sensor)


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
        cursor.execute(schema)
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
