from socket import *
serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.
print ("TCP Server\n")
connectionSocket, addr = serverSocket.accept()
sentence = connectionSocket.recv(65000)

received = str(sentence,"utf-8")
print ("Received From Client: ", received)

capitalizedSentence = sentence.upper() # processamento

connectionSocket.send(capitalizedSentence)

sent = str(capitalizedSentence,"utf-8")
print ("Sent back to Client: ", sent)
connectionSocket.close()