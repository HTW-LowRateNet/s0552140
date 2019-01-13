import time
import random

class Message:
    rn = "\r\n"
    def __init__(self,type,msgID,ttl,hops,sendAddr,destAddr,msg):
        self.type = type
        if msgID == "":
            self.msgID = str(hex(random.randint(0,65535)))
            self.msgID = self.msgID.replace("0x","",1).upper().zfill(4)
        else:
            self.msgID= msgID
        self.ttl = ttl
        self.hops = hops
        self.sendAddr = sendAddr.zfill(4)
        self.destAddr = destAddr.zfill(4)
        self.msg = msg
        
    @classmethod
    def from_array(class_object,message):
        payload = ",".join(message[9:])
        payload = payload.replace("\n","",1)
        return class_object(message[3],message[4],message[5],message[6],message[7],message[8],payload)
        
  
    def messageSize(self):
        str = self.getMessage()
        size = len(str)
        return size
           
    def getMessage(self):
        string = self.type+","+self.msgID+","+self.ttl+","+self.hops+","+self.sendAddr+","+self.destAddr+","+self.msg+","
        return string
    
    def sendMsgForwarding(self,sio):
        print(self.getMessage())
        tempHops = int(self.hops)+1
        self.hops = str(tempHops)
        time.sleep(1)
        print('Forwarding Message: '+self.getMessage())
        time.sleep(.500)
        sio.write('AT+SEND='+str(self.messageSize())+'\r\n')
        sio.flush()
        time.sleep(.500)
        sio.write(self.getMessage())
        sio.flush()
        
    def send(self,sio,iteration):
        while iteration > 0:
            print(self.getMessage())
            time.sleep(.500)
            sio.write('AT+SEND='+str(self.messageSize())+'\r\n')
            sio.flush()
            time.sleep(1)
            sio.write(self.getMessage())
            sio.flush()
            print("SENDED: "+self.getMessage())
            iteration = iteration -1