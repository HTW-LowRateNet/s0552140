import serial
import io
import time
import random
import Node as node
from _thread import start_new_thread

ser = serial.Serial ("/dev/ttyS0")#Open named port)
ser.timeout = 0.1
ser.baudrate = 115200

read = ""
message = []

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

def readSerialLine():
    global read
    global message
    while 1:
        read = sio.readline()
        if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 4:
                message = tempMessage 
            
start_new_thread(readSerialLine,())

test = node.Node("New",ser,"",[])
test.config()
i= 4
while i>=0:
    test.adrDiscovery(read,i)
    print(i)
    if test.state != "New":
        break
    i=i-1

test.sendAlive()

#Eingabe für die Tastatur
while 1:          
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
        #print(">>"+sio.readline())
  
ser.close()