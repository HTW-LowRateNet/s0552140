import serial
import io
import string
import threading
import time

          
      
ser = serial.Serial('/dev/ttyS0',timeout=None)
ser.baudrate = 115200
print(ser.name)



def send():
  print(ser.is_open)
  time.sleep(2)
  ser.write('AT SEND = 5')
  ser.write('Hallo')
  time.sleep(2)
  print("insend")
  
  
def read():
  while True:
   #print("read")
   ser.write(b'AT\r\n')
   print(ser.is_open)
   data =ser.readline()
   print(data)
  
send()  
read()
#Crate Thread 2 Send
#tSend = threading.Thread(target=send)
#Creatin Thread 1 Read
#tRead = threading.Thread(target=read)

#Starten der Threads
#tSend.start()
#tRead.start()


