from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# List of connected clients
# Each client in the list will be a tuple: (client_socket, aes_key)
clients = []

# Function to encrypt message using AES
def encrypt_message(key, message):
    """
    Encrypts a message using AES in CBC mode.

    Args:
        key (bytes): The AES key.
        message (str): The message to encrypt.

    Returns:
        bytes: The IV concatenated with the ciphertext.
    """
    cipher = AES.new(key, AES.MODE_CBC)
    # Pad the message to be a multiple of AES block size, then encode to bytes
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message using AES
def decrypt_message(key, encrypted_message):
    """
    Decrypts an AES encrypted message.

    Args:
        key (bytes): The AES key.
        encrypted_message (bytes): The IV concatenated with the ciphertext.

    Returns:
        str: The decrypted message.
    """
    # Extract IV (initialization vector) from the beginning of the encrypted message
    iv = encrypted_message[:AES.block_size]
    # Extract ciphertext from the rest of the encrypted message
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt the ciphertext and unpad it, then decode to string
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to handle individual client connections
def handle_client(client_socket, client_address):
    """
    Handles communication with a single connected client.
    This includes key exchange and message relaying.

    Args:
        client_socket (socket.socket): The socket object for the client connection.
        client_address (tuple): The address (IP, port) of the client.
    """
    print(f"Connected with {client_address}")

    try:
        # 1. Send server's public key to client for secure AES key exchange
        client_socket.send(server_key.publickey().export_key(format='PEM'))

        # 2. Receive client's public key (not strictly needed for this chat,
        #    but good for mutual authentication/encryption)
        client_received_key = RSA.import_key(client_socket.recv(2048))

        # 3. Generate a unique AES key for message encryption with this client
        aes_key = get_random_bytes(16)

        # 4. Encrypt the generated AES key using the client's public key
        cipher_rsa = PKCS1_OAEP.new(client_received_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        # 5. Add this client's socket and its unique AES key to the global clients list
        clients.append((client_socket, aes_key))
        print(f"AES key exchanged with {client_address}. Total clients: {len(clients)}")

        # 6. Main loop for receiving and relaying messages from this client
        while True:
            # Receive encrypted message from the client
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message: # If no data received, client has disconnected
                break

            # Decrypt the received message
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")

            # Check for 'exit' command to close connection
            if decrypted_message.lower() == "exit":
                print(f"Client {client_address} requested to exit.")
                break

            # Send the decrypted message to all other connected clients
            for client_sock, client_aes_key in clients:
                if client_sock != client_socket: # Don't send back to the sender
                    try:
                        # Encrypt the message with the recipient's AES key
                        encrypted_to_send = encrypt_message(client_aes_key, decrypted_message)
                        client_sock.send(encrypted_to_send)
                    except Exception as e:
                        print(f"Error sending message to {client_sock.getpeername()}: {e}")
                        # Optionally handle disconnected clients here (e.g., remove from list)

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # Ensure client is removed and socket is closed when done or an error occurs
        if (client_socket, aes_key) in clients:
            clients.remove((client_socket, aes_key))
        client_socket.close()
        print(f"Connection with {client_address} closed. Remaining clients: {len(clients)}")


# Main server loop to accept incoming client connections
print("Server is listening for connections...")
while True:
    try:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle this client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        # Start the thread
        client_thread.start()
    except Exception as e:
        print(f"Error accepting new connection: {e}")
        break # Exit the server loop on critical error

