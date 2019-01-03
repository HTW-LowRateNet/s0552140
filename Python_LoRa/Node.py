import serial
import io
import time
import random
import Message as ms
import threading
class Node:
    resAddr = ""
    addrAnfrage = False
    
    def __init__(self,state,ser,addr,nabore):
        self.state = state
        self.addr = addr
        self.ser = ser
        self.nabore = nabore
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
        globalMessage = ms.Message.from_array(["","","","","","","","","",""])
        self.knownAddr = []
        self.mssgQueue = []
           
    def config(self):
        self.state = "New"
        print("Basic Configuration..")
        self.sio.write('AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4\r\n')
        self.sio.flush()
        message = ms.Message("CDIS","","2","1",self.addr,"FFFF","")
        message.send(self.sio,3)
        time.sleep(.400)
        self.setAddr()
        
    def adrDiscovery(self,i):
        print("Addr Discovery..")
        time.sleep(1)
        print(self.globalMessage)
        while i>=0:
            print(i)
            if self.globalMessage.type != "":
               if self.globalMessage.type == "ALIV":
                    print("I am not the Captain")
                    self.state = "Node"
                    print("Get message from coordinator")
                    self.getAddrFromKoordinator()
                    break
            if self.state == "New" and i==0:
                self.state= "Koordinator"
                self.setAddr()
            time.sleep(1)
            i=i-1
     
    def setAddr(self):
        tempAddr = ""
        if self.state == "New":
            tempAddr = str(hex(random.randint(11,255)))
            tempAddr = tempAddr.replace("0x","",1).upper()
            print("New Addr:"+ tempAddr)
        if self.state == "Koordinator":
            tempAddr = "0"
        if self.state == "Node":
            tempAddr = self.addr
            message = ms.Message("AACK","","0","0",self.addr,self.globalMessage.sendAddr,"")
            message.send(self.sio,2)
            time.sleep(1)
    
        self.addr = tempAddr
        self.sio.write('AT+ADDR='+tempAddr+'\r\n')
        self.sio.flush()
        print("Adresse: "+self.addr+" wurde Eingestellt!")
        
    def getAddrFromKoordinator(self):
        print("get Addr from Coordinator")
        message = ms.Message("ADDR","","0","0",self.addr,"0000","")
        message.send(self.sio,3)
        time.sleep(2)
        haveAdress = 1
        while haveAdress == 1:
            if self.globalMessage.type == "ADDR":
                print(self.globalMessage.msg)
                self.state = "Node"
                self.addr = self.globalMessage.msg
                self.setAddr()
                haveAdress= 0
                time.sleep(1)
    
     
    def generateAndSendAddr(self):
        global resAddr
        global addrAnfrage
        addrAnfrage = True
        tempAddr = str(hex(random.randint(101,65534)))
        tempAddr = tempAddr.replace("0x","",1).upper()
        if self.knownAddr != []:
            print("In if ADDR")
            if self.addrIsKnown(tempAddr)==True:
                self.generateAndSendAddr()
        print("GLOBAL_MESSAGE: "+self.globalMessage.sendAddr+self.globalMessage.type)
        message = ms.Message("ADDR","","1","1",self.addr,self.globalMessage.sendAddr,tempAddr)
        resAddr = tempAddr
        print("send ADDR: "+ tempAddr)
        message.send(self.sio,2)
    
    def addrIsKnown(self,tempAddr):
        if self.knownAddr == []:
            return False
        for i in self.knownAddr:
                if i == tempAddr:
                    return True
                else:
                    return False
    def msgIsAlreadyStored(self,msg):
        print("MSG: "+msg.msgID)
        erg = False
        if self.mssgQueue == []:
            return False
        if self.mssgQueue != []:
            for m in self.mssgQueue:
                print(m.type)
                if m.msgID == msg.msgID: #and m.sendAddr == msg.sendAddr:
                    erg = True
                else:
                    erg = False
        return erg
    
    def saveKnownAddr(self):
        global resAddr
        resAddr = self.globalMessage.sendAddr
        if self.addrIsKnown(resAddr) == False:
            print("Save Addr!! "+self.globalMessage.sendAddr)
            self.knownAddr.append(resAddr)
            print(self.knownAddr)
        
             
    def sendAlive(self,times):
        global addrAnfrage
        if addrAnfrage == True:
            return
        while times > 0 and addrAnfrage == False :
            message = ms.Message("ALIV","","0","0",self.addr,"FFFF","I am the captain!")
            message.send(self.sio,times)
            time.sleep(3)
            print(message.messageSize())
            times = times -1