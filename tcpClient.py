from socket import *

serverName = 'localhost'
serverPort = 12000

# Create a IPv4, TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

sentence = input('Input a lowercase sentence: ')
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)
print('From Server uppercase sentence: ', modifiedSentence.decode())
clientSocket.close()