import os
import sys
from pathlib import Path
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from cores.database_api import DatabaseAPI

signin_UI = Path(__file__).parent.parent / 'ui' / 'signin_screen.ui'


class LoginScreen(QtWidgets.QDialog):
    """ Provide a login screen to increase the user privacy """

    def __init__(self: "LoginScreen") -> None:
        """ initialize the application with its UI and utility methods """
        super(LoginScreen, self).__init__()
        os.chdir(os.path.dirname(__file__))
        uic.loadUi(signin_UI, self)
        self.db_obj = DatabaseAPI()
        self.load_user_data()
        self.show()
        self.login_button.clicked.connect(self.login)

    def load_user_data(self):
        user_data = self.db_obj.get_user_by_id(1)
        user_name = user_data[1]
        user_image = user_data[3]
        self.signin_user_img.setPixmap(QPixmap(user_image))
        self.signin_user_img.setScaledContents(True)
        self.login_user_line.setText(user_name)

    def login(self):
        """ Validate the provided username and password and call the main application. """
        login_username = self.login_user_line.text()
        login_password = self.login_password_line.text()
        if len(login_password) < 1:
            self.status.setText("Please Enter Password!")
        else:
            user_id, user_name, password, image = self.db_obj.get_user_by_id(1)
            # Validate username and password.
            if login_username == user_name and login_password == password:
                self.accept()
            else:
                self.status.setText("Invalid Password !!")


if __name__ == "__main__":
    # Calling our application :)
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    app.exec_()
