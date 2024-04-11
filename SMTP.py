# Carina Vlaun 
# Computer Networks 2024
# SMTP Python Lab 

from socket import *
import ssl

msg = "\r\nI love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
port = 587 #port number for gmail 

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM) # AF_INET - used for gmail communication SOCK_STREAM - used for TCP 
clientSocket.connect((mailserver, port))

recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# Start TLS connection to the internet
tls_command = "STARTTLS\r\n"
clientSocket.send(tls_command.encode())
recv_tls = clientSocket.recv(1024)
print(recv_tls)

# Wrap the socket with both SSL and TLS for a secure connection to the internet 
clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

# Send AUTH LOGIN command for mail authentication for gmail 
auth_login = "AUTH LOGIN\r\n"
clientSocket.send(auth_login.encode())
recv_auth = clientSocket.recv(1024)
print(recv_auth)

# Send mail username converted to base 64
username = "Y2FyaW5hdmxhdW4xNg\r\n"
clientSocket.send(username.encode())
recv_user = clientSocket.recv(1024)
print(recv_user)

# Send mail password converted to base 64
password = "b2NnbSBjcGJzIG1rbG8gdmxnbA\r\n"
clientSocket.send(password.encode())
recv_pass = clientSocket.recv(1024)
print(recv_pass)

# Send MAIL FROM command and print server response.
mail_from = "MAIL FROM: <carinavlaun16@gmail.com>\r\n"
clientSocket.send(mail_from.encode())
recv2 = clientSocket.recv(1024)
print(recv2)

# Send RCPT TO command and print server response.
rcpt_to = "RCPT TO: <cvlaun@mail.stmarytx.edu>\r\n"
clientSocket.send(rcpt_to.encode())
recv3 = clientSocket.recv(1024)
print(recv3)

# Send DATA command and print server response.
data_command = "DATA\r\n"
clientSocket.send(data_command.encode())
recv_data = clientSocket.recv(1024)
print(recv_data)

# Send message data.
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())

# Send QUIT command and get server response.
quit_command = "QUIT\r\n"
clientSocket.send(quit_command.encode())
recv_quit = clientSocket.recv(1024)
print(recv_quit)