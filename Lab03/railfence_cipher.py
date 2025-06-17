import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow 
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.butEN.clicked.connect(self.call_api_encrypt)
        self.ui.butDE.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": self.ui.PLTEXT.toPlainText(),
            "key": self.ui.KEY.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.CITEXT.setPlainText(data.get("encrypted_text", ""))

                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                QMessageBox.warning(self, "Error", f"Encryption failed: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Network error: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": self.ui.CITEXT.toPlainText(),
            "key": self.ui.KEY.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.PLTEXT.setPlainText(data.get("decrypted_text", ""))

                QMessageBox.information(self, "Success", "Decrypted Successfully")
            else:
                QMessageBox.warning(self, "Error", f"Decryption failed: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Network error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("Rail Fence Cipher")
    window.show()
    sys.exit(app.exec_())
