from dataclasses import dataclass
import socket
import json
from json import JSONEncoder


@dataclass
class SensorData:
    sample_str: str
    sample_int: int
    sample_float: float


class SensorDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def start_client():
    data = SensorData('testing strings', 100_000, 123.456)
    outbound_data = json.dumps(data, indent=4, cls=SensorDataEncoder)

    host, port = 'localhost', 4000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Connected to:", (host, port))
        sock.sendall(bytes(outbound_data, 'utf-8'))
        print("Message sent:", outbound_data)
    sock.close()


def main():
    start_client()


if __name__ == '__main__':
    main()
