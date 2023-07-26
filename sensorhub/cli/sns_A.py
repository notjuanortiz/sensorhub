import socket 
import random
import pickle
import time
from dataclasses import dataclass
print ("test\n\n")

@dataclass
class Sensor:
    info : -100 
    name : "name"

def start_client(name):
    #data = Sensor(-10, "sensor_A")
    #print (data.info)
    #out_byte_string =  pickle.dumps(data) #"pickled" byte string
    cycle = 10
    while True:

        host, port = 'localhost', 4000
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        #startTime = time.process_time()
        #endTime = time.process_time()
        #while (endTime - startTime) < 10:
        #cycle = 5
        #while True:
            #sock.connect((host, port))
            cycle -= 1
            print("Connected to:", (host, port))
            #sock.sendall(bytes(outbound_data, 'utf-8'))

            temp = random.randint(1,100)
            data = Sensor(temp, "sensor_"+name)
            print (data.info)
            out_byte_string =  pickle.dumps(data) #"pickled" byte string

            #sock.sendall(out_byte_string)
            sock.send(out_byte_string)
            print("Message sent:", out_byte_string)
            time.sleep(0.5)
            #endTime = time.process_time()
            #if cycle < 1: break
            #sock.close()

        sock.close()
        if cycle < 1: break

def main():
##    start_client()

    sen00 = Sensor(0, "")
    print (sen00.info)
    temp = random.randint(1,100)
    print (temp)
    sen00.info= temp
    print (sen00.info)

    start_client("A")

if __name__ == '__main__':
    main()
