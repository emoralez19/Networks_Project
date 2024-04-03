#UDPPingerServer.py
#Code given by Dr. Barsoum
#the random library is needed to generate randomized lost packets
import random
from socket import *

#Create a UDP packet
#SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
#Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
    #Generate a random number in the range 0 to 10
    rand = random.randint(0,10)
    #Receive the client packet as well as the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    #Capitalize the message from the client
    message = message.upper()
    #If rand is less than 4, consider the packet as lost and do not respond
    if rand < 4:
        continue
    #Otherwise the server will respond
    serverSocket.sendto(message,address)
