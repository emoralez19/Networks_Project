#UDPClient.py
#Code by Eli Moralez
#Libraries needed to create a UDP socket and to calculate Round Trip Time
from socket import *
import time

#Create a UDP socket for the client side
clientSocket = socket(AF_INET, SOCK_DGRAM)

#Assign IP address and port number
serverName = '127.0.0.1'
serverPort = 12000

#Ping the server 10 times
for i in range (10):
    #sentTime used in round trip time calculation
    sentTime = time.time()
    message = 'Ping # ' + str(i) + " " + time.ctime(sentTime)  
    print('Sent ' + message)
    try:
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        clientSocket.settimeout(1.0)
        data, server = clientSocket.recvfrom(2048)
        print('Received ' + str(data))
        end = time.time()
        #calculate round trip time for specific packet
        elapsed = end - sentTime
        print('Round Trip Time: ' + str(elapsed) + ' seconds\n')
    except timeout:
        print('# ' + str(i) + ' requested timeout\n')
 

clientSocket.close()
    