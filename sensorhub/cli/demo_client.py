import datetime
import pickle
import random
import socket
import time
from dataclasses import dataclass


@dataclass
class Sensor:
    info: int
    name: str
    time: datetime


def create_sensor_message(sensor_name: str) -> Sensor:
    offset = len(sensor_name) % 31
    random_measurement = random.randint(offset, offset * offset)
    sensor = Sensor(info=random_measurement, name=sensor_name, time=datetime.datetime.now())
    return pickle.dumps(sensor)


def main():
    # server_host = 'localhost'
    server_host = '18.118.17.8'
    server_port = 4000

    # vars
    sensor_name = input("Enter a unique sensor name:")
    interval_in_seconds = int(input("Enter time between messages (in seconds):"))

    # Open TCP connection to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_host, server_port))
        print("\nConnected to:", (server_host, server_port))

        # Continuously send messages until the connection is terminated
        while True:
            message = create_sensor_message(sensor_name)
            sock.sendall(message)
            print('Message sent to: ', server_host, ':', server_port)
            time.sleep(interval_in_seconds)

            response = sock.recv(2048).decode()
            if "error" in response:
                error_type, error_message = response.split(":", 1)
                if error_type == "ValueError":
                    print("ValueError on server:", error_message)
                elif error_type == "DatabaseError":
                    print("DatabaseError on server:", error_message)
                elif error_type == "ServerError":
                    print("ServerError on server:", error_message)
                else:
                    print("Unknown error on server:", error_message)


if __name__ == '__main__':
    main()
