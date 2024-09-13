from socket import *
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


# Função para gerar e salvar chaves RSA
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
   
    # Salvando as chaves em arquivos
    with open("server_private_key.pem", "wb") as f:
        f.write(private_pem)
   
    with open("server_public_key.pem", "wb") as f:
        f.write(public_pem)
   
    return private_key, public_key


# Função para carregar a chave pública do arquivo
def carregar_chave_publica():
    with open("server_public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
    return public_key


# Função para carregar a chave privada do arquivo
def carregar_chave_privada():
    with open("server_private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    return private_key


# Função para criptografar uma mensagem usando RSA
def criptografar_mensagem(mensagem, public_key):
    return public_key.encrypt(
        mensagem.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


# Função para descriptografar uma mensagem usando RSA
def descriptografar_mensagem(mensagem_encriptada, private_key):
    return private_key.decrypt(
        mensagem_encriptada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode("utf-8")


# Função para enviar a chave pública
def enviar_chave_publica(socket, public_key):
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    socket.send(public_pem)


# Função para receber a chave pública
def receber_chave_publica(socket):
    public_key_pem = socket.recv(4096)
    return serialization.load_pem_public_key(public_key_pem, backend=default_backend())


# Configurando o servidor socket
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("TCP Server iniciado e aguardando conexões...\n")


# Gerar e salvar chaves RSA do servidor
private_key, public_key = gerar_chaves_rsa()


# Aceitar uma conexão
connectionSocket, addr = serverSocket.accept()
print(f"Conexão estabelecida com: {addr}")


# Enviar a chave pública do servidor
enviar_chave_publica(connectionSocket, public_key)


# Receber a chave pública do cliente
client_public_key = receber_chave_publica(connectionSocket)


# Receber a mensagem encriptada do cliente
mensagem_encriptada = connectionSocket.recv(65000)


# Descriptografar a mensagem recebida
mensagem_recebida = descriptografar_mensagem(mensagem_encriptada, private_key)
print("Received From Client (Decrypted):", mensagem_recebida)


# Processar a mensagem (converter para maiúsculas)
capitalizedSentence = mensagem_recebida.upper()


# Criptografar a resposta usando a chave pública do cliente
mensagem_encriptada_resposta = criptografar_mensagem(capitalizedSentence, client_public_key)


# Enviar a resposta encriptada de volta ao cliente
connectionSocket.send(mensagem_encriptada_resposta)


print("Sent back to Client (Encrypted).")


# Fechar a conexão
connectionSocket.close()
