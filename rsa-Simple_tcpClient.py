from socket import *
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Função para gerar chaves RSA
def gerar_chaves_rsa():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    # Serializando as chaves para armazenar
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
    with open("private_key.pem", "wb") as f:
        f.write(private_pem)
    
    with open("public_key.pem", "wb") as f:
        f.write(public_pem)

    print("Chaves RSA geradas e salvas em arquivos.")

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


# Gerar chaves RSA (uma vez, ou se não existirem)
gerar_chaves_rsa()

# Configurando o cliente socket
serverName = "192.168.78.169"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Carregar a chave pública
public_key = carregar_chave_publica()

# Solicitar a mensagem do usuário
sentence = input("Input lowercase sentence: ")

# Criptografar a mensagem antes de enviar
mensagem_encriptada = criptografar_mensagem(sentence, public_key)

# Enviar a mensagem encriptada
clientSocket.send(mensagem_encriptada)

# Receber a resposta encriptada
modifiedSentence = clientSocket.recv(65000)

# Carregar a chave privada para descriptografar a resposta
private_key = carregar_chave_privada()

# Descriptografar a resposta
resposta_decriptada = descriptografar_mensagem(modifiedSentence, private_key)

# Exibir a resposta descriptografada
print("Received from Make Upper Case Server: ", resposta_decriptada)

clientSocket.close()
