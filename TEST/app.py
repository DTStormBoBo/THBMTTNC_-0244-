from flask import Flask, render_template, jsonify
import os
import subprocess
import threading

# Khởi tạo Flask app
app = Flask(__name__, template_folder="templates")

# Hàm chạy file Qt ở LAB-03
def run_qt_script(script_filename):
    script_path = os.path.abspath(os.path.join("..", "Lab03", script_filename))
    subprocess.Popen(["python", script_path], shell=True)

# Trang chính
@app.route("/")
def home():
    return render_template("index.html")

# API mở giao diện Qt (trả về JSON, không chuyển trang)
@app.route("/open/caesar")
def open_caesar():
    threading.Thread(target=run_qt_script, args=("caesar_cipher.py",)).start()
    return jsonify({"status": "success", "message": " Caesar"})

@app.route("/open/vigenere")
def open_vigenere():
    threading.Thread(target=run_qt_script, args=("vigenere_cipher.py",)).start()
    return jsonify({"status": "success", "message": " Vigenere "})

@app.route("/open/railfence")
def open_railfence():
    threading.Thread(target=run_qt_script, args=("railfence_cipher.py",)).start()
    return jsonify({"status": "success", "message": " Rail Fence "})

@app.route("/open/playfair")
def open_playfair():
    threading.Thread(target=run_qt_script, args=("playfair_cipher.py",)).start()
    return jsonify({"status": "success", "message": " Playfair Qt"})

# Chạy ứng dụng
if __name__ == "__main__":
    app.run(port=5050, debug=True)
