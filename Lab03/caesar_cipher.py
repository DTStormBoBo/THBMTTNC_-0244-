import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests
from ui.caesar import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.butEN.clicked.connect(self.call_api_encrypt)
        self.ui.butDE.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.PLTEXT.toPlainText(),
            "key": self.ui.KEY.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.CITEXT.setPlainText(data.get("encrypted_message", "Error: No encrypted_message in response"))

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print(f"API Error")
        except requests.exceptions.RequestException as e:
            print("Error : %s" % e.message)
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.CITEXT.toPlainText(),
            "key": self.ui.KEY.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.PLTEXT.setPlainText(data.get("decrypted_message", "Error: No decrypted_message in response"))

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print(f"API Error ")    

        except requests.exceptions.RequestException as e:
            print("Error : %s" % e.message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())