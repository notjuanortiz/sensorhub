import datetime
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
    time : None

def start_client(name, delayTime, readings):

    host, port = 'localhost', 4000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
       sock.connect((host, port))

       while True: #sensor "reading" and sending loop
           readings -= 1
           print("Connected to:", (host, port))
    
           temp = random.randint(1,100)
           timestamp = datetime.datetime.now()
           sensorObject = Sensor(temp, "sensor_"+name, timestamp)
           print (sensorObject.info)
           out_byte_package =  pickle.dumps(sensorObject) #"pickled" byte string

           sock.sendall(out_byte_package )
           print("Message sent:", out_byte_package)
           time.sleep(delayTime)
           if readings < 1: break
    
    print("\nshould have sent the \"closing\" message by now -- short timeout after this")
    time.sleep(2)
    sock.close()

def main():
    start_client(name="D", delayTime=0.5, readings=7)

if __name__ == '__main__':
    main()
