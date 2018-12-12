import serial
import io
import time
import Node as node
from _thread import start_new_thread

ser = serial.Serial ("/dev/ttyS0")#Open named port)
ser.timeout = 0.3
ser.baudrate = 115200

read = ""
message = []

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
test = node.Node("New",ser,"",[])

def readSerialLine():
    global read
    global message
    while 1:
        read = sio.readline()
        if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 5:
                message = tempMessage
                test.globalMessage = message
                test.input()
            
start_new_thread(readSerialLine,())


test.config()
test.globalMessage=[]
#test.input()
i= 1
while i>=0:
    test.adrDiscovery(i)
    print(i)
    if test.state != "New":
        break
    i=i-1

#test.sendAlive()

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