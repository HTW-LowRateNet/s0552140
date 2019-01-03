import serial
import io
import time
import Node as node
import threading
import random
import Message as ms
from _thread import start_new_thread

ser = serial.Serial ("/dev/ttyS0")#Open named port)
ser.timeout = 0.3
ser.baudrate = 115200

read = ""
message = []
resMessage = ""
addrAnfrage = ""

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
node = node.Node("New",ser,"",[])

def readSerialLine():
    global read
    global message
    global resMessage
    while 1:
        read = sio.readline()
        if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 5:
                message = tempMessage
                node.globalMessage = ms.Message.from_array(message)
                resMessage = ms.Message.from_array(message)
                time.sleep(1)
                inputMessage()
            
start_new_thread(readSerialLine,())

def inputMessage():
    global addrAnfrage
    global resMessage
    global message
    global sio
    if node.globalMessage.type != "":
        print("inputNode: "+node.globalMessage.type)
        if node.state == "Koordinator":
            if resMessage.type =="CDIS":
                node.sendAlive(1)
            if resMessage.type=="ADDR":
                addrAnfrage = ms.Message.from_array(message)
                node.generateAndSendAddr()
            if resMessage.type=="AACK":
                node.saveKnownAddr()
            if resMessage.type=="ALIV":
                shutDown()
        if node.state == "Node":
            if resMessage.type == "NRST":
                shutDown()
        if node.state == "Node" or node.state == "Koordinator":
            if resMessage.type != "":
                checkMssgAndStore(resMessage)
                #tCheckMssg = threading.Thread(target = checkMssgAndStore,name ='checkMssgAndStore',args=([resMessage]))
                #tCheckMssg.start()
def checkMssgAndStore(msg):
    global sio
    if node.addr == msg.destAddr:
        print("Du hast eine neue Nachricht: "+msg.msg)
        return
    else:
        if node.msgIsAlreadyStored(msg) == True:
            print("MSSG is alrady stored")
            return
        if node.msgIsAlreadyStored(msg) == False:
            print("append: "+ msg.type)
            node.mssgQueue.append(msg)
            msg.sendMsgForwarding(sio)
            return
            
        
#def sendMessages():
   
        
    

def shutDown():
    if node.state == "Koordinator":
        message = ms.Message("NRST","","0","0",node.addr,"FFFF","")
        message.send(sio,2)
    sleep = random.randint(1,15)
    print("sleepTime: "+str(sleep))
    time.sleep(sleep)
    node.state="New"
    node.globalMessage = ms.Message.from_array(["","","","","","","","","",""])
    tDisc = threading.Thread(target = node.adrDiscovery,name ='addrDiscovery',args=([addrTimes]))
    tDisc.start()

node.globalMessage = ms.Message.from_array(["","","","","","","","","",""])
node.config()
addrTimes = 14
node.adrDiscovery(addrTimes)
#tDisc = threading.Thread(target = node.adrDiscovery,name ='addrDiscovery',args=([addrTimes]))
#tDisc.start()


    
   

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