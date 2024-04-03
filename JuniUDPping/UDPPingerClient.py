#UDPPingerClient.py

from socket import *
import datetime
#send packets to local host ip address
serverName = '127.0.0.1'

#create socket that is IPv4 and UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

#set the timeout for the socket to 1 second
clientSocket.settimeout(1)

#send 10 pings and check for response
for i in range(10):
    

    #set timestamp for when the message is sent
    timeSent = datetime.datetime.now()

    #create messages based on iterator and timestamp
    message = f"ping {i} {timeSent}"
    
    #send message to the server and the port (what, where)
    clientSocket.sendto(message.encode(), (serverName, 12000))

    #test if message is received
    try:        
        #receive message back from server (how many bytes to receive)
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        
        #set timestamp for when the message is received
        timeReceived = datetime.datetime.now()
        
        #calculate the round trip time based on time sent and time received
        rtt = timeReceived - timeSent
        
        #print modified message plus the round trip time
        print("Received: ", modifiedMessage.decode(), f"RTT = {rtt.total_seconds()}s")

    #if no message received within 1 second, print error message and continue
    except:
        print("Request timed out")
   
clientSocket.close()