from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher 
from cipher.vigenere import VigenereCipher 


app = Flask(__name__)
caesar_cipher = CaesarCipher()
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/app/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()

    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/app/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

playfair_cipher = PlayFairCipher()
cipher = PlayFairCipher()

@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route('/app/playfair/encrypt', methods=['POST'])
def encrypt_playfair():
    input_plain_text = request.form['inputPlainText']
    input_key_plain = request.form['inputKeyPlain']
    matrix = cipher.create_playfair_matrix(input_key_plain)
    encrypted_result = cipher.playfair_encrypt(input_plain_text, matrix)
    return render_template('playfair.html',
                           input_plain_text=input_plain_text,
                           input_key_plain=input_key_plain,
                           encrypted_result=encrypted_result)

@app.route('/app/playfair/decrypt', methods=['POST'])
def decrypt_playfair():
    input_cipher_text = request.form['inputCipherText']
    input_key_cipher = request.form['inputKeyCipher']
    matrix = cipher.create_playfair_matrix(input_key_cipher)
    decrypted_result = cipher.playfair_decrypt(input_cipher_text, matrix)
    return render_template('playfair.html',
                           input_cipher_text=input_cipher_text,
                           input_key_cipher=input_key_cipher,
                           decrypted_result=decrypted_result)

railfence_cipher = RailFenceCipher()
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route('/app/railfence/encrypt', methods=['POST'])
def encrypt_railfence():
    input_plain_text = request.form['inputPlainText']
    input_key_plain = int(request.form['inputKeyPlain'])
    encrypted_result = railfence_cipher.rail_fence_encrypt(input_plain_text, input_key_plain)
    return render_template('railfence.html',
                            input_plain_text=input_plain_text,
                            input_key_plain=input_key_plain,
                            encrypted_result=encrypted_result)

@app.route('/app/railfence/decrypt', methods=['POST'])
def decrypt_railfence():
    input_cipher_text = request.form['inputCipherText']
    input_key_cipher = int(request.form['inputKeyCipher']) 
    decrypted_result = railfence_cipher.rail_fence_decrypt(input_cipher_text, input_key_cipher)
    return render_template('railfence.html',
                            input_cipher_text=input_cipher_text,
                            input_key_cipher=input_key_cipher,
                            decrypted_result=decrypted_result)


vigenere_cipher = VigenereCipher()
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route('/app/vigenere/encrypt', methods=['POST'])
def encrypt_vigenere():
    input_plain_text = request.form['inputPlainText']
    input_key_plain = request.form['inputKeyPlain']
    encrypted_result = vigenere_cipher.vigenere_encrypt(input_plain_text, input_key_plain)
    return render_template('vigenere.html',
                            input_plain_text=input_plain_text,
                            input_key_plain=input_key_plain,
                            encrypted_result=encrypted_result)

@app.route('/app/vigenere/decrypt', methods=['POST'])
def decrypt_vigenere():
    input_cipher_text = request.form['inputCipherText']
    input_key_cipher = request.form['inputKeyCipher']
    decrypted_result = vigenere_cipher.vigenere_decrypt(input_cipher_text, input_key_cipher)
    return render_template('vigenere.html',
                            input_cipher_text=input_cipher_text,
                            input_key_cipher=input_key_cipher,
                            decrypted_result=decrypted_result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)