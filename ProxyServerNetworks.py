#Skeleton code provided
#Code finished by Eli Moralez

from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start
serverPort = 14000
tcpSerSock.bind(('', serverPort))
tcpSerSock.listen(1)
# Fill in end

# added try and except to handle closing the sever socket
try:
    while True:
        # Start receiving data from the client
        print('Ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from:', addr)
        message = tcpCliSock.recv(1024) #Fill in start  #Fill in end
        message2 = message.decode('utf-8')
        print(message2)
        # Extract the filename from the given message
        print(message2.split()[1])
        filename = message2.split()[1].partition("/")[2]
        print(filename)
        fileExist = False
        filetouse = "/" + filename
        print(filetouse)
        try:
            # Check whether the file exists in the cache
            with open(filetouse[1:], "rb") as f:
                outputdata = f.read()
                fileExist = True
                print("Requested file found in cache:", filetouse)
            # ProxyServer finds a cache hit and generates a response message
            response = "HTTP/1.0 200 OK\r\n"
            response += "Content-Type: text/html\r\n"
            response += "\r\n"
            #Fill in start
            response += outputdata.decode('utf-8')
            tcpCliSock.send(response.encode())
            #Fill in end
            print('Read from cache')

        # Error handling for file not found in cache
        except IOError:
            if not fileExist:
                print("Requested file NOT found in cache, perform GET to server for file:", filetouse)                
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM) #Fill in start   #Fill in end               
                hostn = filename.replace("www.", "", 1)
                print(hostn)
                try:
                    # Connect to the socket to port 80
                    #Fill in start
                    c.connect((hostn, 80))
                    #Fill in end
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj = c.makefile('rwb', 0)
                    fileobj.write(("GET " + "http://" + filename + " HTTP/1.0\r\n\r\n").encode())
                    fileobj.flush()                    
                    # Read the response into buffer
                    #Fill in start
                    buff = fileobj.read()
                    #Fill in end
                    # Create a new file in the cache for the requested file
                    # Send the response in the buffer to client socket and the corresponding file in the cache
                    with open("./" + filename, "wb") as tmpFile:
                        #Fill in start
                        tmpFile.write(buff)
                        tcpCliSock.send(buff)
                        #Fill in end
                except:
                    print("Illegal request")

            else:
                # HTTP response message for file not found
                #Fill in start
                response = "HTTP/1.0 404 Not Found\r\n"
                response += "Content-Type: text/html\r\n\r\n"
                response += "<html><body><h1>404 Not Found</h1></body></html>"
                tcpCliSock.send(response.encode())
                #Fill in end
        
        #Close the client and server sockets
        tcpCliSock.close()

finally:
    tcpSerSock.close()
