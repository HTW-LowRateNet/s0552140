import serial
import io
import time
import random
import Message as ms
class Node:
    resAddr = ""
    
    def __init__(self,state,ser,addr,nabore):
        self.state = state
        self.addr = addr
        self.ser = ser
        self.nabore = nabore
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
        globalMessage = []
        self.knownAddr = []
        
        
    def input(self):
        print("inputNode: "+self.globalMessage[3])
        if self.state == "Koordinator":
            if self.globalMessage[3]=="CDIS":
                self.sendAlive(3)
            if self.globalMessage[3]=="ADDR":
                self.generateAndSendAddr()
            if self.globalMessage[3]=="AACK":
                self.saveKnownAddr()
        
        
    def config(self):
        self.state = "New"
        print("Basic Configuration..")
        self.sio.write('AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4\r\n')
        self.sio.flush()
        message = ms.Message("CDIS","01msID","2","1",self.addr,"ffff","")
        message.send(self.sio,3)
        time.sleep(1)
        self.setAddr()
        
    def adrDiscovery(self,i):
        print("Addr Discovery..")
        time.sleep(1)
        print(self.globalMessage)
        if len(self.globalMessage)!= 0:
           if self.globalMessage[3] == "ALIV":
                print("I am not the Caption")
                self.state = "Node"
                print("Get message from coordinator")
                self.getAddrFromKoordinator()
                
            
        if self.state == "New" and i== 0:
            self.state= "Koordinator"
            self.setAddr()
        time.sleep(1)
     
    def setAddr(self):
        tempAddr = ""
        if self.state == "New":
            tempAddr = str(random.randint(1,100))           
        if self.state == "Koordinator":
            tempAddr = "0"
        if self.state == "Node":
            tempAddr = self.addr
            message = ms.Message("AACK","1mid","1","1",self.addr,self.globalMessage[7],"")
            message.send(self.sio,1)
            time.sleep(1)
    
        self.addr = tempAddr
        self.sio.write('AT+ADDR='+tempAddr+'\r\n')
        self.sio.flush()
        print("Adresse: "+self.addr+" wurde Eingestellt!")
        
    def getAddrFromKoordinator(self):
        print("get Addr from Coordinaator")
        message = ms.Message("ADDR","0","0","0",self.addr,"0","")
        message.send(self.sio,3)
        time.sleep(2)
        haveAdress = 1
        while haveAdress == 1:
            if self.globalMessage[3] == "ADDR":
                print(self.globalMessage[9])
                self.state = "Node"
                self.addr = self.globalMessage[9]
                self.setAddr()
                haveAdress= 0
                time.sleep(1)
    
     
    def generateAndSendAddr(self):
        global resAddr
        tempAddr = str(random.randint(101,600))
        if self.knownAddr != []:
            print("In if ADDR")
            for i in self.knownAddr:
                if i == tempAddr:
                    self.generateAndSendAddr()
        message = ms.Message("ADDR","0mID","1","1",self.addr,self.globalMessage[7],tempAddr)
        resAddr = tempAddr
        message.send(self.sio,2)
    
    def saveKnownAddr(self):
        global resAddr
        if resAddr == self.globalMessage[7]:
            print("Save Addr!! "+resAddr)
            self.knownAddr.append(resAddr)
            resAddr = ""
            print(self.knownAddr)
             
    def sendAlive(self,times):
        while times > 0:
            time.sleep(1)
            message = ms.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
            message.send(self.sio,1)
            print(message.messageSize())
            times = times -1