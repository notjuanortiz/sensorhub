import datetime
import pickle
import random
import socket
import threading
import time
from dataclasses import dataclass

terminate = False


@dataclass
class Sensor:
    info: int
    name: str
    time: datetime


def create_sensor_message(sensor_name: str) -> Sensor:
    random_measurement = random.randint(1, 100)
    sensor = Sensor(info=random_measurement, name=sensor_name, time=datetime.datetime.now())
    print("\n\tsensor reading: ", sensor.info)
    return pickle.dumps(sensor)


def user_input_thread():
    print("Press ENTER to terminate the connection.")
    input()
    global terminate
    terminate = True


def main():
    #server_host = 'localhost'
    server_host = '18.118.17.8'
    server_port = 4000

    # vars
    sensor_name = "sensor_Juan"
    interval_in_seconds = 10

    global terminate
    terminate = False

    # Create nonblocking thread to handle user input
    input_thread = threading.Thread(target=user_input_thread)
    input_thread.start()

    # Open TCP connection to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_host, server_port))
        print("\nConnected to:", (server_host, server_port))

        # Continuously send messages until the connection is terminated
        while not terminate:
            message = create_sensor_message(sensor_name)
            sock.sendall(message)
            print("sensor object sent:\n", message)
            time.sleep(interval_in_seconds)

            if terminate:
                break

        print("Terminating the connection.")


if __name__ == '__main__':
    main()