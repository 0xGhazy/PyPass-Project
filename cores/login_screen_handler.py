import os
import sys
from pathlib import Path
from PyQt5 import QtWidgets, uic
from cores.database_api import DatabaseAPI
from cores.logsystem import LogSystem


signin_UI = Path(__file__).parent.parent / 'ui' / 'signin_screen.ui'

class LoginScreen(QtWidgets.QDialog):
    """ Provide a login screen to increase the user privacy """

    def __init__(self: "LoginScreen") -> None:
        """ initialize the application with its UI and utility methods """
        super(LoginScreen, self).__init__()
        os.chdir(os.path.dirname(__file__))
        # loading .ui design file.
        uic.loadUi(signin_UI, self)
        self.db_obj = DatabaseAPI()
        # Load the first username to the username field
        self.login_user_line.setText(self.get_first_user())
        self.login_button.clicked.connect(self.login)
        self.show()

    def get_first_user(self):
        db_response = self.db_obj.db_query(f"SELECT * FROM Users")
        if db_response is not None:
            username = list(db_response)[0][1]
            return username

    def login(self):
        """ Validate the provided username and password and call the main application. """
        login_username = self.login_user_line.text()
        login_password = self.login_password_line.text()
        if len(login_password) < 1:
            self.status.setText("Please Enter Password!")
        else:
            db_response = self.db_obj.db_query(f"SELECT * FROM Users")
            user_id, user_name, password, _ = db_response[0]
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
