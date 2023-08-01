import os
import pickle
import socketserver
import sys

import psycopg2
from dotenv import load_dotenv

from sensorhub import PostgreSQLConnector, Sensor
from sensorhub.sensor_management import SensorService


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
                print("\n\tClosing connection from: ", self.client_address)
                break

            print("\nMessage received from: ", self.client_address,
                  "\tMessage size: ", msg_size, type(messages))
            sensor_data: Sensor = pickle.loads(messages)

            # deserialize sensor (matches clients data structure)
            sensor_data.measurement = sensor_data.info
            sensor_data.taken_on = sensor_data.time
            print(sensor_data)

            service = SensorService(PostgreSQLConnector())
            service.save(sensor_data)


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
