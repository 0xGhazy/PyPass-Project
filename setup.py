import os
import sys
from pathlib import Path
from cores.database_api import DatabaseAPI
from cores.encryption import EncryptionHandler
from platform import platform

BASE_DIR = Path(__file__).resolve().parent


def check_python_version():
    # check if python 3 is installed
    if sys.version_info[0] != 3:
        print("[-] Python 3.x is required.")
        return 0
    else:
        return 1


def install_reqs():
    # install requirements from req.txt
    print(platform())
    if "Windows" in platform():
        os.system("pip install -r req.txt")
        os.system("cls")
    else:
        os.system("pip3 install -r req.txt")
        os.system("clear")
    print("\n Requirements installed successfully \n")


def user_account_setup():
    db_obj = DatabaseAPI()
    # sec_obj = EncryptionHandler()
    # sec_obj.generate_key()
    username = os.getlogin()
    password = input("Password>> ")
    default_image = BASE_DIR / "ui" / "default.png"
    data = {
        "User_Name": f"{username}",
        "User_Password": f"{password}",
        "User_Image": f"{default_image}"
    }
    db_obj.add_user(data)
    print("User Account Created!")


if __name__ == '__main__':
    # change cwd to the setup.py script directory
    os.chdir(os.path.dirname(__file__))
    if check_python_version():
        try:
            install_reqs()
            user_account_setup()
        except Exception as error_message:
            print(f"[-] Error Massage:\n{error_message}\n")
    else:
        exit()
