#Serial imported for Serial communication
import serial                                                              
#Required to use delay functions   
import time            
#Create Serial port object called ArduinoUnoSerialData time.sleep(2)
#wait for 2 secounds for the communication to get established                                                    
ArduinoUnoSerial = serial.Serial('com4',9600)                                                                    

while 1:         
    #get input from user
    var = raw_input()
    #if the value is 1                                                       
    if (var == '1'):          
        #send 1 to the arduino's Data code                                               
        ArduinoUnoSerial.write('1')                             
        print ("LED turned ON")         
        time.sleep(1)          
    if (var == '0'): #if the value is 0
        #send 0 to the arduino's Data code         
        ArduinoUnoSerial.write('0')                
        print ("LED turned OFF")         
        time.sleep(1)
    if (var == 'fine and you'): #if the answer is (fine and you)
        #send 0 to the arduino's Data code          
        ArduinoUnoSerial.write('0')   
        print ("I'm fine too, Are you Ready to !!!")         
        print ("Type 1 to turn ON LED and 0 to turn OFF LED")         
        time.sleep(1)
