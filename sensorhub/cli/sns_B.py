import datetime
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
    time : None

def start_client(name):

    host, port = 'localhost', 4000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
       sock.connect((host, port))

       startTime = time.process_time()
       cycle = 50 
       while True:
           cycle -= 1
           print("Connected to:", (host, port))
    
           temp = random.randint(1,100)
           timestamp = datetime.datetime.now()
           data = Sensor(temp, "sensor_"+name, timestamp)
           print (data.info)
           out_byte_string =  pickle.dumps(data) #"pickled" byte string

           #pkSize = sys.getsizeof(out_byte_string)
           #print(pkSize)
           ##sock.send(pkSize) 

           #sock.send(out_byte_string)
           sock.sendall(out_byte_string)
           print("Message sent:", out_byte_string)
           time.sleep(.2)
           endTime = time.process_time()
           print("\ttime elapsed: ", (endTime - startTime))
           if cycle < 1: break
           if 10000*(endTime - startTime) > 20: break
    
    print("should have sent the \"closing\" message by now -- short timeout after this")
    time.sleep(1)
    print("long timeout after this")
    time.sleep(5)
    sock.close()

def main():
##    start_client()

    start_client("B")

if __name__ == '__main__':
    main()
