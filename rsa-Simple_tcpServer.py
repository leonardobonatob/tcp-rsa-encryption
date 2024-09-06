from socket import *
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Função para carregar a chave pública
def carregar_chave_publica():
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
    return public_key

# Função para carregar a chave privada
def carregar_chave_privada():
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    return private_key

# Função para criptografar uma mensagem usando RSA
def criptografar_mensagem(mensagem, public_key):
    mensagem_encriptada = public_key.encrypt(
        mensagem.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_encriptada

# Função para descriptografar uma mensagem usando RSA
def descriptografar_mensagem(mensagem_encriptada, private_key):
    mensagem_decriptada = private_key.decrypt(
        mensagem_encriptada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_decriptada.decode("utf-8")

# Configurando o servidor socket
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("TCP Server iniciado e aguardando conexões...\n")

# Aceitar uma conexão
connectionSocket, addr = serverSocket.accept()
print(f"Conexão estabelecida com: {addr}")

# Carregar a chave privada para descriptografar as mensagens recebidas
private_key = carregar_chave_privada()

# Receber a mensagem encriptada do cliente
mensagem_encriptada = connectionSocket.recv(65000)

# Descriptografar a mensagem recebida
mensagem_recebida = descriptografar_mensagem(mensagem_encriptada, private_key)
print("Received From Client (Decrypted):", mensagem_recebida)

# Processar a mensagem (converter para maiúsculas)
capitalizedSentence = mensagem_recebida.upper()

# Carregar a chave pública para criptografar a resposta
public_key = carregar_chave_publica()

# Criptografar a resposta
mensagem_encriptada_resposta = criptografar_mensagem(capitalizedSentence, public_key)

# Enviar a resposta encriptada de volta ao cliente
connectionSocket.send(mensagem_encriptada_resposta)

print("Sent back to Client (Encrypted).")

# Fechar a conexão
connectionSocket.close()
