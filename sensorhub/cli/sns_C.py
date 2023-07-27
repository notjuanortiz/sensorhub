import socket 
import random
import pickle
import sys
import time
from dataclasses import dataclass
print ("test\n\n")

@dataclass
class Sensor:
    info : -100 
    name : "name"

def start_client(name):

    host, port = 'localhost', 4000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
       sock.connect((host, port))

       startTime = time.process_time()
       cycle = 50
       while True:
           #sock.connect((host, port))
           cycle -= 1
           print("Connected to:", (host, port))
           #sock.sendall(bytes(outbound_data, 'utf-8'))
    
           temp = random.randint(1,100)
           data = Sensor(temp, "sensor_"+name)
           print (data.info)
           out_byte_string =  pickle.dumps(data) #"pickled" byte string

           #pkSize = sys.getsizeof(out_byte_string)
           #print(pkSize)
           ##sock.send(pkSize) 
           #time.sleep(0.1)

           sock.sendall(out_byte_string)
           #sock.send(out_byte_string)
           print("Message sent:", out_byte_string)
           time.sleep(.3)
           endTime = time.process_time()
           print("\ttime elapsed: ", (endTime - startTime))
           if cycle < 1: break
           if 10000*(endTime - startTime) > 15: break
           #sock.close()
    
    print("should have sent the \"closing\" message by now -- short timeout after this")
    time.sleep(1)
    print("long timeout after this")
    time.sleep(5)
    sock.close()

def main():
##    start_client()

    start_client("C")

if __name__ == '__main__':
    main()
