from socket import *
serverName = "192.168.78.169"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input("Input lowercase sentence: ")
clientSocket.send(bytes(sentence, "utf-8"))
modifiedSentence = clientSocket.recv(65000)
text = str(modifiedSentence,"utf-8")
print ("Received from Make Upper Case Server: ", text)
clientSocket.close()