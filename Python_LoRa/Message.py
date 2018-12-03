import time

class Message:
    rn = "\r\n"
    def __init__(self,type,msgID,ttl,hops,ownAddr,destAddr,msg):
        self.type = type
        self.msgID = msgID
        self.ttl = ttl
        self.hops = hops
        self.ownAddr = ownAddr
        self.destAddr = destAddr
        self.msg = msg
        
    
    def messageSize(self):
        str = self.getMessage()
        size = len(str)
        return size
           
    def getMessage(self):
        string = self.type+","+self.msgID+","+self.ttl+","+self.hops+","+self.ownAddr+","+self.destAddr+","+self.msg+","
        return string
    
    def send(self,sio,dest):
        time.sleep(1)
        sio.write('AT+SEND='+str(self.messageSize())+'\r\n')
        sio.flush()
        time.sleep(1)
        sio.write(self.getMessage())
        
        
        
    #def sendMsg(self):