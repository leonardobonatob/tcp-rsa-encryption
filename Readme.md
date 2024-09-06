
# TCP Client-Server with RSA Encryption

This project demonstrates a simple TCP client-server communication with RSA encryption. The client sends an encrypted message to the server, and the server decrypts it, processes the message (converts it to uppercase), and sends back an encrypted response. Both the client and the server utilize asymmetric RSA keys for encryption and decryption.

## Features

- **RSA Encryption/Decryption**: Uses RSA 4096-bit keys for secure communication.
- **Socket Programming**: Implements TCP-based communication between client and server.
- **Asymmetric Cryptography**: Public key for encryption and private key for decryption.

## Prerequisites

- Python 3.6+
- `cryptography` library

### Install dependencies:

```bash
pip install cryptography
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/leonardobonatob/tcp-rsa-encryption.git
cd tcp-rsa-encryption
```

### 2. Generate RSA Keys

Before running the client or server, you need to generate RSA keys (public and private). The client script will automatically generate them on the first run. Ensure that both `public_key.pem` and `private_key.pem` are present in the working directory.

### 3. Running the Server

Run the server on the desired host (e.g., `192.168.78.169` on port `1300`).

```bash
python Simple_tcpServer.py
```

The server will:
- Listen for incoming client connections.
- Decrypt the received message using the private RSA key.
- Process the message (convert it to uppercase).
- Encrypt the response using the public RSA key and send it back.

### 4. Running the Client

Once the server is running, start the client on the same machine or a different one connected to the network.

```bash
python Simple_tcpClient.py
```

The client will:
- Take user input (a sentence) and encrypt it using the public RSA key.
- Send the encrypted message to the server.
- Receive the encrypted response from the server, decrypt it using the private RSA key, and display the message.

## Code Overview

### Client (`Simple_tcpClient.py`)

- **Key Generation**: Automatically generates 4096-bit RSA keys (`public_key.pem` and `private_key.pem`).
- **Encryption**: Encrypts the user input with the public RSA key.
- **Decryption**: Decrypts the response from the server using the private RSA key.

### Server (`Simple_tcpServer.py`)

- **Decryption**: Decrypts the received message from the client using the private RSA key.
- **Processing**: Converts the received message to uppercase.
- **Encryption**: Encrypts the processed message using the public RSA key and sends it back to the client.

## Example Workflow

1. **Client**: Encrypts a message (e.g., "hello world") and sends it to the server.
2. **Server**: Decrypts the message, processes it (e.g., "HELLO WORLD"), encrypts the response, and sends it back.
3. **Client**: Decrypts the server's response and displays it.

## File Structure

```
├── Simple_tcpClient.py        # Client-side code
├── Simple_tcpServer.py        # Server-side code
├── public_key.pem             # Public key for encryption
├── private_key.pem            # Private key for decryption
├── README.md                  # Documentation
```

## Security

This project uses RSA for secure communication. With RSA:
- The **public key** is used to encrypt messages.
- The **private key** is used to decrypt messages.

Keep your **private key** safe and never share it. The **public key** can be shared with anyone who needs to send encrypted messages.

## Troubleshooting

- Ensure both the client and server have access to the correct RSA key files.
- Verify network connectivity between the client and server.
- Make sure the `cryptography` library is installed properly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. This project was made by Faculdade Engenheiro Salvador Arena students: Leonardo Bonato Bizaro, Nathan Bitu de Oliveira, Ariel Pereira dos Santos, and Pedro de Souza Silva.

---
