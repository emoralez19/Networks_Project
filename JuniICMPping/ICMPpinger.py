from socket import *
import os
import sys
import struct
import time
import select
import binascii 

ICMP_ECHO_REQUEST = 8

# def checksum(string): 
#     csum = 0
#     countTo = (len(string) // 2) * 2 
#     count = 0
#     while count < countTo:
#         thisVal = ord(string[count+1]) * 256 + ord(string[count]) 
#         csum = csum + thisVal 
#         csum = csum & 0xffffffff 
#         count = count + 2

#     if countTo < len(string):
#         csum = csum + ord(string[len(string) - 1])
#         csum = csum & 0xffffffff 

#     csum = (csum >> 16) + (csum & 0xffff)
#     csum = csum + (csum >> 16)
#     answer = ~csum 
#     answer = answer & 0xffff 
#     answer = answer >> 8 | (answer << 8 & 0xff00)
#     return answer

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    string = bytearray(string, 'ascii') #specifed encoding as ascii
    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + string[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


#**********EMILY********
def receiveOnePing(mySocket, ID, timeout, destAddr): 
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft) 
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."
        
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        #Fill in start
        
        # get header information from the received packet, including TTL
        icmpheader = recPacket[20:28] 
        ttl = struct.unpack("B", recPacket[8:9])[0]

        # unpack header fields
        type, code, checksum, packetId, sequenceNo = struct.unpack("bbHHh", icmpheader)

        
        # check if the received packet ID matches the expected ID
        if packetId == ID:
            bytesInDouble = struct.calcsize("d") # get the size of a double in bytes
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            rtt=timeReceived - timeSent

            # display the extracted header information and RTT
            print(f"The header received in the ICMP reply (from: {destAddr}) is type: {type}, code: {code},"
                  f"checksum: {checksum}, packet ID: {packetId}, sequence number: {sequenceNo}, "
                  f"time to live: {ttl}\nRTT is: " + str(rtt))
            return
        
        
        #Fill in end
        
        timeLeft = timeLeft - howLongInSelect 
        if timeLeft <= 0:
            return "Request timed out."
        

#********BARSOUM**********

# def receiveOnePing(mySocket, ID, timeout):
#     global pkgRec, RTT

#     timeLeft = timeout
#     while True:
#         startedSelect = time.time()
#         whatReady = select.select([mySocket], [], [], timeLeft)
#         howLongInSelect = time.time() - startedSelect

#         if not whatReady[0]:  # Timeout
#             return "Request timed out. whatReady"

#         timeReceived = time.time()
#         recPacket, _ = mySocket.recvfrom(1024)

#         # Fetch the ICMP header from the IP packet
#         icmpHeader = recPacket[20:28]
#         recType, recCode, recChksum, recID, recSeq = struct.unpack('bbHHh', icmpHeader)

#         if ID == recID:
#             bytesInDouble = struct.calcsize('d')
#             timeData = struct.unpack('d', recPacket[28:28 + bytesInDouble])[0]
#             RTT.append(timeReceived - timeData)
#             pkgRec += 1
#             return timeReceived - timeData

#         timeLeft -= howLongInSelect
#         if timeLeft <= 0:
#             return "Request timed out."
        

#*******MINE**********

# def receiveOnePing(mySocket, ID, timeout, destAddr):
#     timeLeft = timeout

#     while 1: 
#         startedSelect = time.time()
#         whatReady = select.select([mySocket], [], [], timeLeft)
#         howLongInSelect = (time.time() - startedSelect)
#         if whatReady[0] == []: # Timeout
#             print(whatReady[0])
#             return "Request timed out. whatready"
        
#         timeReceived = time.time() 
#         recPacket, addr = mySocket.recvfrom(1024)
    
#         #Fill in start

#         icmpHeader = recPacket[20:28]
#         icmpType, code, checksum, packetID, sequence = struct.unpack('bbHHh', icmpHeader)

#         #check if packet is an echo reply (type = 0) and is of the same ID as the request
#         if icmpType == 0 and code == 0 and packetID == ID:
#             # Calculate the round-trip time

#             # get data from struct and extract the time the data was sent
#             timeSent = struct.unpack("d", recPacket[28:])[0]
#             # find the round trip time and convert into seconds
#             delay = (timeReceived - timeSent) * 1000
#             return delay

#         #Fill in end

#         timeLeft = timeLeft - howLongInSelect
#         if timeLeft <= 0:
#             return "Request timed out.timeleft "

def sendOnePing(mySocket, destAddr, ID):

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(str(header + data))


    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout): 
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw

    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    while 1 :
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)# one second
    return delay
    
ping('127.0.0.1')