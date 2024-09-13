from socket import *
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


def gerar_chaves_rsa():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem


def carregar_chave_publica(pem_data):
    return serialization.load_pem_public_key(pem_data, backend=default_backend())


def carregar_chave_privada(pem_data):
    return serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())


def criptografar_mensagem(mensagem, public_key):
    return public_key.encrypt(
        mensagem.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def descriptografar_mensagem(mensagem_encriptada, private_key):
    return private_key.decrypt(
        mensagem_encriptada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode("utf-8")


def send_public_key(socket, public_key_pem):
    socket.send(public_key_pem)


def receive_public_key(socket):
    public_key_pem = socket.recv(4096)
    return carregar_chave_publica(public_key_pem)


private_pem, public_pem = gerar_chaves_rsa()


serverName = "10.1.70.33"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


# Enviar chave pública
send_public_key(clientSocket, public_pem)


# Receber chave pública do servidor
server_public_key = receive_public_key(clientSocket)


# Solicitar a mensagem do usuário
sentence = input("Input lowercase sentence: ")


# Criptografar a mensagem antes de enviar
mensagem_encriptada = criptografar_mensagem(sentence, server_public_key)


# Enviar a mensagem encriptada
clientSocket.send(mensagem_encriptada)


# Receber a resposta encriptada
modifiedSentence = clientSocket.recv(65000)


# Descriptografar a resposta (usando a mesma chave privada que gerou o par de chaves)
private_key = carregar_chave_privada(private_pem)
resposta_decriptada = descriptografar_mensagem(modifiedSentence, private_key)


# Exibir a resposta descriptografada
print("Received from Make Upper Case Server: ", resposta_decriptada)


clientSocket.close()
