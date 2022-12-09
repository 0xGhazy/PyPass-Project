import os
import sys
import getpass
from cores.database_api import DatabaseAPI
from platform import platform


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
    username = os.getlogin()
    password = getpass.getpass()
    db_obj.db_query(f"""INSERT INTO Users (User_Name, User_Password)
                        VALUES ('{username}', '{password}');""")
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
