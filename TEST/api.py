import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lab02_path = os.path.abspath(os.path.join(current_dir, "../Lab02"))
sys.path.append(lab02_path)

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

from flask import Flask, request, jsonify

app = Flask(__name__)

# Caesar
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    encrypted = caesar_cipher.encrypt_text(data["plain_text"], int(data["key"]))
    return jsonify({"encrypted_message": encrypted})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    decrypted = caesar_cipher.decrypt_text(data["cipher_text"], int(data["key"]))
    return jsonify({"decrypted_message": decrypted})

# Vigenère
vigenere_cipher = VigenereCipher()

@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    data = request.json
    encrypted = vigenere_cipher.vigenere_encrypt(data["plain_text"], data["key"])
    return jsonify({"encrypted_text": encrypted})

@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    data = request.json
    decrypted = vigenere_cipher.vigenere_decrypt(data["cipher_text"], data["key"])
    return jsonify({"decrypt_text": decrypted})

# Rail Fence
railfence_cipher = RailFenceCipher()

@app.route("/api/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    data = request.json
    encrypted = railfence_cipher.rail_fence_encrypt(data["plain_text"], int(data["key"]))
    return jsonify({"encrypted_text": encrypted})

@app.route("/api/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    data = request.json
    decrypted = railfence_cipher.rail_fence_decrypt(data["cipher_text"], int(data["key"]))
    return jsonify({"decrypt_text": decrypted})

# Playfair
playfair_cipher = PlayFairCipher()

@app.route("/api/playfair/creatematrix", methods=["POST"])
def playfair_matrix():
    data = request.json
    matrix = playfair_cipher.create_playfair_matrix(data["key"])
    return jsonify({"playfair_matrix": matrix})

@app.route("/api/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    data = request.json
    matrix = playfair_cipher.create_playfair_matrix(data["key"])
    encrypted = playfair_cipher.playfair_encrypt(data["plain_text"], matrix)
    return jsonify({"encrypted_text": encrypted})

@app.route("/api/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    data = request.json
    matrix = playfair_cipher.create_playfair_matrix(data["key"])
    decrypted = playfair_cipher.playfair_decrypt(data["cipher_text"], matrix)
    return jsonify({"decrypted_text": decrypted})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
