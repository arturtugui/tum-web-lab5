from socket import *
import sys

if len(sys.argv) != 3:
    print("Usage: python go2web.py <server_name> <server_port>")
    sys.exit(1)

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a IPv4, TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establish a connection to the server
clientSocket.connect((serverName, serverPort))

# Send an HTTP GET request to the server
http_request = '''GET / HTTP/1.1\r\n
            Host: google.com\r\n
            \r\n'''

clientSocket.sendall(http_request.encode())

# Receive the HTTP response from the server
http_response_binary = b""
while True:
    chunk = clientSocket.recv(4096)
    if not chunk:
        break
    http_response_binary += chunk

http_response = http_response_binary.decode(errors="replace")

# Extract response information
header_end = http_response.find("\r\n\r\n")
http_response_header = http_response[:header_end]

status_line = http_response_header.splitlines()[0]
protocol = status_line.split()[0]
status_code = status_line.split()[1]
status_message = " ".join(status_line.split()[2:])

#   Split header before and after "Date: " and pick the part after
#   Split the remaining string at the first occurrence of "\r\n" to get the date value
date = http_response_header.split("Date: ")[1].split("\r\n")[0]

expiration = http_response_header.split("Expires: ")[1].split("\r\n")[0]

print(f"Protocol: {protocol}")
print(f"Status Code: {status_code}")
print(f"Status Message: {status_message}")
print(f"Date: {date}")
print(f"Expiration: {expiration}")

clientSocket.close()