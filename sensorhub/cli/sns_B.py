import datetime
import socket
import random
import pickle
import time
from dataclasses import dataclass


@dataclass
class Sensor:
    info: int
    name: str
    time: datetime


def start_client(name, delay_time, readings):
    host, port = 'localhost', 4000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        print("\nConnected to:", (host, port))
        print("Press ENTER to start data feed.")
        input()  # pauses till some keyboard entry

        while True:  # sensor "reading" and sending loop
            readings -= 1

            temp = random.randint(1, 100)
            timestamp = datetime.datetime.now()
            sensor_object = Sensor(temp, "sensor_" + name, timestamp)
            print(sensor_object.info)
            out_byte_package = pickle.dumps(sensor_object)  # "pickled" byte string

            sock.sendall(out_byte_package)
            print("Message sent:", out_byte_package)
            time.sleep(delay_time)
            if readings < 1:
                break
    sock.close()


def main():
    start_client(name="B", delay_time=0.2, readings=13)


if __name__ == '__main__':
    main()
