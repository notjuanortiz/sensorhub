import logging
import os
import pickle
import socketserver
import sys

import psycopg2
from dotenv import load_dotenv

from sensor import Sensor, SensorService

service = SensorService()

logging.basicConfig(filename='server_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class SensorDataRequestHandler(socketserver.StreamRequestHandler):
    """Created once per connection to the server"""
    buffer_size = 2048

    def handle(self):
        try:
            sensor = (None, None, None)
            print("\nClient address: ", self.client_address)
            while True:
                messages = self.connection.recv(self.buffer_size)
                if not messages:
                    print("\nClosing connection from: ", self.client_address)
                    break
                print("\nMessage received from: ", self.client_address)
                sensor: Sensor = pickle.loads(messages)

                # deserialize sensor (matches clients data structure)
                sensor.measurement = sensor.info
                sensor.taken_on = sensor.time
                print("Found:", sensor)
                service.save(sensor)
        except pickle.UnpicklingError as e:
            logging.error("Error while unpickling data: %s", e)
            self.connection.close()
        except psycopg2.Error as e:
            logging.error("Error while saving data to database: %s", e)
            self.connection.close()
        except Exception as e:
            logging.error("Unknown error: %s", e)
            self.connection.close()


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

    try:
        with socketserver.ThreadingTCPServer((host, port), SensorDataRequestHandler) as server:
            print('Sensor management listening on:', (host, port))
            server.serve_forever()
    except OSError as e:
        print("Error starting server:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
