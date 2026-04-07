from socket import *

serverName = 'google.com'
serverPort = 80

# Create a IPv4, TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

http_request = '''GET / HTTP/1.1\r\n
            Host: google.com\r\n
            \r\n'''

clientSocket.sendall(http_request.encode())

http_response_binary = b""
while True:
    chunk = clientSocket.recv(4096)
    if not chunk:
        break
    http_response_binary += chunk

http_response = http_response_binary.decode(errors="replace")

header_end = http_response.find("\r\n\r\n")
http_response_header = http_response[:header_end]
print(http_response_header)

clientSocket.close()