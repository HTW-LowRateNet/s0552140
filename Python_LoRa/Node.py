import serial
import io
import time
import random
import Message as ms
class Node:
    def __init__(self,state,ser,addr,nabore):
        self.state = state
        self.addr = addr
        self.ser = ser
        self.nabore = nabore
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
        
    def config(self):
        self.state = "New"
        print("Basic Configuration..")
        self.sio.write('AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4\r\n')
        self.sio.flush()
        time.sleep(1)
        self.setAddr()
        
    def adrDiscovery(self, message,i):
        print("Addr Discovery..")
        self.sio.write('AT+RX\r\n')
        self.sio.flush()
        time.sleep(1)
        if len(message)!= 0:
           if message[3] == "ALIV":
                print("I am not the Caption")
                self.state = "Node"
                print("Get message from coordinator")
                self.setAddr()
                #ASK for a new Adress
                setAddr()
            
        if self.state == "New" and i== 0:
            self.state= "Koordinator"
            self.setAddr()
           # coordinatorSendNotify()
        time.sleep(1)
     
    def setAddr(self):
        tempAddr = ""
        if self.state == "New":
            tempAddr = str(random.randint(1,100))           
        if self.state == "Koordinator":
            tempAddr = "0"
        if self.state == "Node":
            #type,msgID,ttl,hops,ownAddr,destAddr,msg
            #? Adressanfrage an Koordinator
            message = ms.Message("ADDS","0","0",self.addr,"0")
            print(message.toString)
            tempAddr = "200"
    
        self.addr = tempAddr
        self.sio.write('AT+ADDR='+tempAddr+'\r\n')
        self.sio.flush()
        print("Adresse: "+self.addr+" wurde Eingestellt!")
        
    def sendAlive(self):
        while self.state == "Koordinator":
            message = ms.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
            message.send(self.sio,"ffff")
            print(message.messageSize())      