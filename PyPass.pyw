import os
import sys
import string
import random
import datetime
import pyperclip
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QLineEdit, QFileDialog
# importing applications cores
from cores.encryption import EncryptionHandler
from cores.database_api import DatabaseAPI
from cores.qr_handler import QRHandler
from cores.login_screen_handler import LoginScreen

BASE_DIR = Path(__file__).resolve().parent
main_UI = BASE_DIR / "ui" / "MainWindowUI.ui"

# change this when you want to add new platform, append it in lower case :)
SUPPORTED_PLATFORMS = ["facebook", "codeforces", "github",
                       "gmail", "hackerranck", "medium",
                       "outlook", "quora", "twitter",
                       "udacity", "udemy", "university", "wordpress", "lol", "stack overflow", "linkedin"]

SUPPORTED_FILES_FORMATS = ["7z", "cpp", "c", "cs", "css", "xlsx", "exe", "flv", "html",
                           "ai", "java", "js", "jpg", "mp3", "mp4", "pdf", "php",
                           "png", "pptx", "psd", "py", "word", "rar", "txt", "sql"]

BUTTONS_STYLE = {
    "normal-style": """QPushButton{background-color:#251B37;color: white;}
                       QPushButton:hover {background:linear-gradient(to bottom, #5cbf2a 5%, #44c767 100%);
                       background-color:#372948;}
                       QPushButton:active {position:relative;top:3px;}""",
    "clicked-style": "background-color:#372948;color:white;"
}


class PyPass(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super(PyPass, self).__init__()
        self.qr_handle = None
        os.chdir(os.path.dirname(__file__))
        uic.loadUi(main_UI, self)
        self.repo_url = "https://github.com/0xGhazy/PyPass"
        self.outer_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.inner_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget_2')
        self.settings_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget_3')
        self.outer_tabWidgets.tabBar().setVisible(False)
        self.inner_tabWidgets.tabBar().setVisible(False)
        self.settings_tabWidgets.tabBar().setVisible(False)
        # self.show()
        self.app_path = Path(__file__).resolve().parent
        self.database_obj = DatabaseAPI()
        self.security_obj = EncryptionHandler()
        self.signin_window = LoginScreen()
        self.show_password_is_clicked = True  # if show password is clicked
        if self.signin_window.exec_() == QtWidgets.QDialog.Accepted:
            self.display_accounts(self.accounts_list_edit)
            self.display_accounts(self.accounts_list_view)
            self.accounts_page.clicked.connect(self.outer_accounts_page)
            self.files_page.clicked.connect(self.outer_files_page)
            self.saveed_accounts_page.clicked.connect(self.accounts_view_page)
            self.edit_accounts_page.clicked.connect(self.accounts_edit_page)
            self.accounts_list_view.itemClicked.connect(self.accounts_list_view_click)
            self.settings_page.clicked.connect(self.outer_setting_page)
            self.insert_account_data.clicked.connect(self.add_new_account)
            self.update_account_data.clicked.connect(self.edit_account)
            self.star_my_repo.clicked.connect(self.release_note_action)
            self.show_password.clicked.connect(self.show_hide_password)
            self.delete_account_data.clicked.connect(self.delete_account)
            self.accounts_list_edit.itemClicked.connect(self.fill_account_data)
            self.files_list_view.itemClicked.connect(self.files_list_view_clicked)
            self.import_key_btn.clicked.connect(self.import_key)
            self.import_file_btn.clicked.connect(self.import_file)
            self.export_file_btn.clicked.connect(self.export_file)
            self.restore_file_btn.clicked.connect(self.file_restore)
            self.export_key_btn.clicked.connect(self.export_key)
            self.profile_browse.clicked.connect(self.browse_image)
            self.update_profile.clicked.connect(self.update_profile_data)
            self.preview_image()
            self.load_profile_data()
            self.show()

    # ------------------------------------- Navigation Buttons -------------------------------------

    # Outer Widget navigations
    def outer_accounts_page(self) -> None:
        self.outer_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.outer_tabWidgets.setCurrentIndex(0)
        # change button style after click
        self.accounts_page.setStyleSheet(BUTTONS_STYLE["clicked-style"])
        self.files_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.settings_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.accounts_view_page()

    def outer_files_page(self) -> None:
        self.outer_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.outer_tabWidgets.setCurrentIndex(1)
        # change button style after click
        self.accounts_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.files_page.setStyleSheet(BUTTONS_STYLE["clicked-style"])
        self.settings_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.fill_files_list_view()

    def outer_setting_page(self) -> None:
        self.outer_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.outer_tabWidgets.setCurrentIndex(2)
        # Display the currant key path
        key_path = self.app_path / "cores" / "security_key.key"
        self.enc_key_edit.setText(f" {str(key_path)}")
        # change button style after click
        self.accounts_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.files_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.settings_page.setStyleSheet(BUTTONS_STYLE["clicked-style"])
        self.load_profile_data()

    def release_note_action(self):
        os.system(f"explorer {self.repo_url}")

    # Inner Widget Navigation
    def accounts_view_page(self):
        self.inner_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget_2')
        self.inner_tabWidgets.setCurrentIndex(0)
        # update the buttons style
        self.saveed_accounts_page.setStyleSheet(BUTTONS_STYLE["clicked-style"])
        self.edit_accounts_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.display_accounts(self.accounts_list_view)

    def accounts_edit_page(self):
        self.inner_tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget_2')
        self.inner_tabWidgets.setCurrentIndex(1)
        # update the buttons style
        self.saveed_accounts_page.setStyleSheet(BUTTONS_STYLE["normal-style"])
        self.edit_accounts_page.setStyleSheet(BUTTONS_STYLE["clicked-style"])
        self.display_accounts(self.accounts_list_edit)
        self.clear_accounts_data()

    # ---------------------------------------------------------------------------------------------

    # Accounts view page methods ------------------------------------------------------------------
    def accounts_list_view_click(self):
        account_index = int(self.accounts_list_view.currentRow())
        selected_account = self.database_obj.list_accounts()[account_index]
        try:
            plain_password = self.security_obj.decrypt(selected_account[3].encode())
            pyperclip.copy(plain_password.decode())
            self.qr_handle = QRHandler()
            self.qr_handle.generate_qr(plain_password.decode(), "photo.png")
            # Reading qr photo in Pixmap and Append the pixmap to QLabel
            self.qr_image_obj.setPixmap(QPixmap("photo.png"))
            self.qr_image_obj.setScaledContents(True)
            # [+] Remove the image from the path.
            os.remove("photo.png")
            self.statusBar().showMessage("[+] Password is copied successfully")
        except Exception as error:
            print(error)

    # ---------------------------------------------------------------------------------------------

    # Accounts edit page methods ------------------------------------------------------------------
    def add_new_account(self) -> None:
        """adding new account to database"""
        plat_name = self.edit_account_platform.text()
        account = self.edit_account_email.text()
        plain_password = self.edit_account_password.text()
        # Check for the password strength
        encrypted_password = self.security_obj.encrypt(plain_password.encode())
        new_account = {
            "Platform": plat_name,
            "Account": account,
            "Password": encrypted_password.decode()
        }
        try:
            self.database_obj.add_account(new_account)
            self.statusBar().showMessage("[+] Account added successfully")
        except Exception as error:
            self.statusBar().showMessage("[!] Can't add this account")
            self.log_obj.write_into_log("-", f"{error}")
        self.display_accounts(self.accounts_list_edit)
        self.clear_accounts_data()

    def edit_account(self) -> None:
        """update selected account on database"""
        account_id = self.edit_account_id.text()
        plat_name = self.edit_account_platform.text()
        account = self.edit_account_email.text()
        plain_password = self.edit_account_password.text()
        encrypted_password = self.security_obj.encrypt(plain_password.encode())
        if len(plat_name) != 0 and len(account) != 0 and len(plain_password) != 0:
            update_account = {
                "Platform": plat_name,
                "Account": account,
                "Password": encrypted_password.decode()
            }
            try:
                self.database_obj.update_account(update_account, account_id)
                self.statusBar().showMessage("[+] Account updated successfully")
            except Exception as error:
                self.statusBar().showMessage("[!] Can't update this account")
                self.log_obj.write_into_log("-", f"{error}")
        self.display_accounts(self.accounts_list_edit)
        self.clear_accounts_data()

    def show_hide_password(self):
        icons_path = BASE_DIR / "ui" / "icons" / "Application icons"
        # closed_eye = BASE_DIR / "ui" / "icons" / "closed-eye.png"
        if self.show_password_is_clicked:
            self.edit_account_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password.setText("")
            self.show_password.setIcon(QIcon(os.path.join(r"{0}".format(icons_path), "closed-eye.png")))
            self.show_password_is_clicked = False
        else:
            self.edit_account_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password.setText("")
            self.show_password.setIcon(QIcon(os.path.join(r"{0}".format(icons_path), "open-eye.png")))
            self.show_password_is_clicked = True

    def delete_account(self) -> None:
        """delete selected account from database"""
        account_id = self.edit_account_id.text()
        self.database_obj.delete_account_by_id(account_id)
        self.display_accounts(self.accounts_list_edit)
        self.statusBar().showMessage("[+] Account removed successfully!")
        self.clear_accounts_data()

    def fill_account_data(self):
        account_index = int(self.accounts_list_edit.currentRow())
        selected_account = self.database_obj.list_accounts()[account_index]
        account_id, platform, account, password = selected_account
        # fill the account fields
        self.edit_account_id.setText(str(account_id))
        self.edit_account_platform.setText(str(platform))
        self.edit_account_email.setText(str(account))
        plain_password = self.security_obj.decrypt(password).decode()
        self.edit_account_password.setText(str(plain_password))

    def clear_accounts_data(self):
        self.edit_account_id.setText("")
        self.edit_account_platform.setText("")
        self.edit_account_email.setText("")
        self.edit_account_password.setText("")

    # ---------------------------------------------------------------------------------------------

    # Handling Methods in setting page ------------------------------------------------------------
    def import_key(self):
        key_file, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'All Files (*.*)')
        if len(key_file) < 1:
            pass
        else:
            # Read the key.
            with open(key_file, "rb") as k_file:
                content = k_file.read()
            # Write The new key.
            key_path = self.app_path / "cores" / "security_key.key"
            with open(key_path, "wb") as k_file:
                k_file.write(content)
        # self.log_obj.write_into_log("+", f"A new key has been imported")
        self.statusBar().showMessage("[+] Key is imported successfully")

    def export_key(self):
        exported_key_path, _ = QFileDialog.getSaveFileName(self, "Save File", "security_key.key")
        key_file = self.app_path / "cores" / "security_key.key"
        # Read the key.
        with open(key_file, "rb") as k_file:
            content = k_file.read()
        # Write The new key.
        with open(exported_key_path, "wb") as k_file:
            k_file.write(content)
        # self.log_obj.write_into_log("+", f"The key is exported at {exported_key_path}")
        self.statusBar().showMessage(f"[+] Your key is exported successfully @ {exported_key_path}")

    # User profile page methods
    def preview_image(self):
        user = self.database_obj.get_user_by_id(1)
        user_image = user[3]
        self.user_profile_preview.setPixmap(QPixmap(user_image))
        self.user_profile_preview.setScaledContents(True)

    def browse_image(self):
        user_image_path = BASE_DIR / "ui" / "user_image"
        image_file, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'All Files (*.*)')
        image_name = image_file.split("/")[-1]
        if len(image_file) < 1:
            return
        else:
            with open(image_file, "rb") as image_file_obj:
                content = image_file_obj.read()
            os.chdir(user_image_path)
            with open(image_name, "wb") as image_file_obj:
                image_file_obj.write(content)
            new_image_path = user_image_path / image_name
            if os.path.isfile(str(new_image_path)):
                self.database_obj.update_user_image(str(new_image_path), 1)
                self.preview_image()
            self.statusBar().showMessage(f"[+] Your profile image updated successfully")

    def update_profile_data(self):
        self.preview_image()
        new_username = self.username_input.text()
        self.database_obj.update_username(new_username, 1)
        self.load_profile_data()
        self.statusBar().showMessage(f"[+] Your username is updated successfully")

    def load_profile_data(self):
        user_profile = self.database_obj.get_user_by_id(1)
        user_name = user_profile[1]
        user_image = user_profile[3]
        # set fields
        self.user_image.setPixmap(QPixmap(user_image))
        self.user_image.setScaledContents(True)
        self.username_lbl.setText(user_name)
        self.username_input.setText(user_name)

    # ---------------------------------------------------------------------------------------------

    # Handling Files methods ----------------------------------------------------------------------
    def files_list_view_clicked(self):
        file_index = int(self.files_list_view.currentRow())
        selected_file = self.database_obj.list_files()[file_index]
        # Fill file data
        self.file_id.setText(str(selected_file[0]))
        self.file_name.setText(str(selected_file[1]))
        self.file_directory.setText(str(selected_file[2]))
        self.file_size.setText(str(selected_file[3]))
        self.file_date_time.setText(str(selected_file[4]))
        self.encrypted_name.setText(str(selected_file[5]))

    def fill_files_list_view(self):
        self.files_list_view.clear()
        data = self.database_obj.list_files()
        icons_path = os.path.join(os.path.dirname(__file__), "ui", "icons", "Files Icons")
        for record in data:
            file_name = record[1]
            ext_name = file_name.split(".")[1]
            if ext_name in SUPPORTED_FILES_FORMATS:
                icon = QtGui.QIcon(os.path.join(icons_path, f"{ext_name}.png"))
            else:
                icon = QtGui.QIcon(os.path.join(icons_path, f"file.png"))
            item = QtWidgets.QListWidgetItem(icon, f" {file_name}")
            self.files_list_view.addItem(item)

    def import_file(self):
        save_path = BASE_DIR / "saved-files"
        file, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'All Files (*.*)')
        if len(file) > 0:
            with open(file, "rb") as file_reader:
                content = file_reader.read()

            # prepare files attributes
            time_now = datetime.datetime.now()
            random_6_letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
            random_file_name = random_6_letters + str(int(datetime.datetime.timestamp(time_now)))
            final_enc_name = f"{random_file_name}.Enc-Py-Pass"
            file_name = file.split("/")[-1]
            file_directory = os.path.dirname(file)
            file_size_in_bytes = os.path.getsize(file)

            new_file = {
                "File_Name": file_name,
                "File_Directory": file_directory,
                "File_Size": file_size_in_bytes,
                "Insertion_Date": f"{time_now}",
                "File_Encrypted_Name": final_enc_name
            }
            # Handling file Content
            enc_file_content = self.security_obj.encrypt(content)
            enc_file_path = save_path / final_enc_name
            if os.path.isfile(random_file_name):
                self.statusBar().showMessage(f"[+] Please try Again")
            else:
                try:
                    with open(f"{enc_file_path}", "wb") as encFile:
                        encFile.write(enc_file_content)
                    if os.path.isfile(enc_file_path):
                        os.remove(file)
                        self.database_obj.add_file(new_file)
                    self.statusBar().showMessage(f"[+] File added successfully")
                except Exception as error:
                    print(error)
                    self.statusBar().showMessage(f"[+] This file is already exist")
        self.fill_files_list_view()

    def export_file(self):
        selected_file_id = self.file_id.text()
        selected_file = self.database_obj.get_file_by_id(selected_file_id)
        file_name = selected_file[1]
        encrypted_name = selected_file[-1]
        exported_file_path, _ = QFileDialog.getSaveFileName(self, "Save File", file_name)
        enc_file_path = BASE_DIR / "saved-files" / encrypted_name
        if os.path.isfile(enc_file_path):
            try:
                with open(enc_file_path, "rb") as fileReader:
                    content = fileReader.read()
                    plain_content = self.security_obj.decrypt(content)
                    with open(exported_file_path, "wb") as writer:
                        writer.write(plain_content)
                    if os.path.isfile(exported_file_path):
                        # Delete File from DB
                        self.database_obj.delete_file_by_id(selected_file_id)
                        self.statusBar().showMessage(f"[+] File exported successfully")
            except Exception as error:
                print(error)
        self.fill_files_list_view()

    def file_restore(self):
        selected_file_id = self.file_id.text()
        selected_file = self.database_obj.get_file_by_id(selected_file_id)
        file_name = selected_file[1]
        directory = selected_file[2]
        final_file = os.path.join(directory, file_name)
        encrypted_name = selected_file[-1]
        enc_file_path = BASE_DIR / "saved-files" / encrypted_name
        if os.path.isdir(directory) and os.path.isfile(enc_file_path):
            try:
                with open(enc_file_path, "rb") as reader:
                    enc_content = reader.read()
                    content = self.security_obj.decrypt(enc_content)
                    with open(final_file, "wb") as writer:
                        writer.write(content)
                self.database_obj.delete_file_by_id(selected_file_id)
                self.statusBar().showMessage(f"[+] File restored successfully")
                self.fill_files_list_view()
            except Exception as error:
                print(error)
    # ---------------------------------------------------------------------------------------------

    # Utilities methods ---------------------------------------------------------------------------
    def display_accounts(self, list_obj) -> None:
        list_obj.clear()
        """append all database accounts to QListWidget on accounts page."""
        icons_path = os.path.join(os.path.dirname(__file__), "ui", "icons", "socialIcons")
        data = self.database_obj.list_accounts()
        for row in data:
            icon = QtGui.QIcon(os.path.join(icons_path, f"{row[1].lower()}.png"))
            if f"{row[1].lower()}" in SUPPORTED_PLATFORMS:
                item = QtWidgets.QListWidgetItem(icon, f"{row[2]}")
                list_obj.addItem(item)
            else:
                icon = QtGui.QIcon(os.path.join(icons_path, f"user.png"))
                item = QtWidgets.QListWidgetItem(icon, f"{row[2]}")
                list_obj.addItem(item)
    # ---------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # calling our application :)
    app = QtWidgets.QApplication(sys.argv)
    window = PyPass()
    app.exec_()
