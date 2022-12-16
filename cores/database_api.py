import os
import sqlite3


class DatabaseAPI:
    """
    DatabaseAPI class provides a formal way to interact with the project database.

    Attributes
    ----------
        _db_name : str
            first name of the person
        _connection : None
            family name of the person

    Methods
    -------
        db_connect(self) -> None
        is_connected(self) -> bool
        create_tables(self) -> bool
        add_account(self, account: dict)
        delete_account(self, account_id: str)
        update_account(self, new_data: dict, account_id: str)
        get_account_by_id(self, account_id: str)
        list_accounts(self)

        add_file(self, file: dict)
        delete_file_by_id(self, file_id: int)
        update_file(self, new_data: dict, file_id: int)
        get_file_by_id(self, file_id: int)
        list_files(self)
    """

    def __init__(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self._db_name = "PyPassdb.sqlite3"
        self._connection = self.db_connect()
        self.create_tables()

    def db_connect(self) -> sqlite3:
        try:
            return sqlite3.connect(self._db_name)
        except Exception as error:
            raise Exception(f"[-] Error Message:\n{error}\n")

    def is_connected(self) -> bool:
        if self._connection is None:
            return False
        return True

    def create_tables(self):
        try:
            self._do_database_action("""
            CREATE TABLE IF NOT EXISTS Accounts (
                "ID"	integer,
                "Platform"	TEXT NOT NULL,
                "Account"	TEXT NOT NULL,
                "Password"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                UNIQUE("Platform","Account"));
            """)

            self._do_database_action("""
            CREATE TABLE IF NOT EXISTS Users (
                "User_ID"	integer,
                "User_Name"	TEXT NOT NULL,
                "User_Password"	TEXT NOT NULL,
                "User_Image"	TEXT,
                UNIQUE("User_Name","User_Password"),
                PRIMARY KEY("User_ID" AUTOINCREMENT));
            """)

            self._do_database_action("""
            CREATE TABLE IF NOT EXISTS Files (
                "File_ID"	INTEGER,
                "File_Name"	TEXT NOT NULL,
                "File_Directory"	TEXT NOT NULL,
                "File_Size"	INTEGER NOT NULL,
                "Insertion_Date"	TEXT NOT NULL,
                "File_Encrypted_Name"	TEXT NOT NULL,
                PRIMARY KEY("File_ID" AUTOINCREMENT),
                UNIQUE("File_Name","File_Directory")
                );
            """)

        except Exception as error:
            raise Exception(f"[-] Error Message:\n{error}\n")

    def _do_database_action(self, query: str) -> None:
        cursor = self._connection.cursor()
        cursor.execute(f"{query}")
        self._connection.commit()

    def _get_database_data(self, query: str) -> list:
        cursor = self._connection.cursor()
        response = cursor.execute(f"{query}")
        return list(response)

    def db_query(self, query):
        return self._get_database_data(query)

    # Account methods ------------------------------------------------------------------------
    def add_account(self, account: dict):
        self._do_database_action(
            f"""INSERT INTO Accounts (Platform, Account, Password)
            VALUES ('{account['Platform']}', '{account['Account']}', '{account['Password']}');
            """)

    def delete_account_by_id(self, account_id: str):
        self._do_database_action(f"DELETE FROM Accounts WHERE id = {account_id};")

    def update_account(self, new_data: dict, account_id: str):
        self._do_database_action(
            f"""UPDATE Accounts SET Platform = '{new_data['Platform']}',
                                    Account = '{new_data['Account']}',
                                    Password = '{new_data['Password']}'
                                    WHERE ID = {account_id};
            """)

    def get_account_by_id(self, account_id: str):
        response = self._get_database_data(f"SELECT * FROM Accounts WHERE ID = {account_id};")
        return list(response)[0]

    def list_accounts(self):
        response = self._get_database_data(f"SELECT * FROM Accounts")
        return list(response)

    # Files Methods ------------------------------------------------------------------------

    def add_file(self, file: dict):
        self._do_database_action(
            f"""INSERT INTO Files (File_Name, File_Directory, File_Size,Insertion_Date, File_Encrypted_name)
                           VALUES ('{file['File_Name']}',
                                   '{file['File_Directory']}',
                                   '{file['File_Size']}',
                                   '{file['Insertion_Date']}',
                                   '{file['File_Encrypted_Name']}');
            """)

    def delete_file_by_id(self, file_id: int):
        self._do_database_action(f"DELETE FROM Files WHERE File_ID = {file_id};")

    def update_file(self, new_data: dict, file_id: int):
        self._do_database_action(
            f"""UPDATE Files SET File_Name = '{new_data['File_Name']}',
                                 File_Directory = '{new_data['File_Directory']}',
                                 File_Size = '{new_data['File_Size']}',
                                 Insertion_Date = '{new_data['Insertion_Date']}',
                                 File_Encrypted_name = '{new_data['File_Encrypted_Name']}'
                                 WHERE File_ID = {file_id};
            """)

    def get_file_by_id(self, file_id: int):
        response = self._get_database_data(f"SELECT * FROM Files WHERE File_ID = {file_id};")
        return list(response)[0]

    def list_files(self):
        response = self._get_database_data(f"SELECT * FROM Files")
        return list(response)

    # Files Methods ------------------------------------------------------------------------

    def update_user_image(self, new_image: str, user_id: int):
        self._do_database_action(
            f"""UPDATE Users SET User_Image = '{new_image}'
                                 WHERE User_ID = {user_id};
            """)

    def update_username(self, user_name: str, user_id: int):
        self._do_database_action(
            f"""UPDATE Users SET User_Name = '{user_name}'
                                 WHERE User_ID = {user_id};
            """)

    def get_user_by_id(self, user_id: int):
        response = self._get_database_data(f"SELECT * FROM Users WHERE User_ID = {user_id};")
        return list(response)[0]

    def add_user(self, user_data: dict):
        self._do_database_action(
            f"""INSERT INTO Users (User_Name, User_Password, User_Image)
                            VALUES ('{user_data['User_Name']}',
                                    '{user_data['User_Password']}',
                                    '{user_data['User_Image']}');
                """)

if __name__ == "__main__":
    x = DatabaseAPI()


#
# """
# CREATE TABLE "Files" (
# 	"f_id"	INTEGER,
# 	"f_name"	TEXT NOT NULL,
# 	"f_dir_name"	TEXT NOT NULL,
# 	"f_size"	INTEGER NOT NULL,
# 	"insertion_date"	TEXT NOT NULL,
# 	"f_enc_name"	TEXT NOT NULL,
# 	PRIMARY KEY("f_id" AUTOINCREMENT)
# );
#
#
#
# CREATE TABLE "Users" (
# 	"u_id"	integer,
# 	"u_name"	TEXT NOT NULL,
# 	"u_password"	TEXT NOT NULL,
# 	"u_image"	TEXT,
# 	UNIQUE("u_name","u_password"),
# 	PRIMARY KEY("u_id" AUTOINCREMENT)
# );
#
# CREATE TABLE "Accounts" (
# 	"ID"	integer,
# 	"Platform"	TEXT NOT NULL,
# 	"Account"	TEXT NOT NULL,
# 	"Password"	TEXT NOT NULL,
# 	PRIMARY KEY("ID" AUTOINCREMENT),
# 	UNIQUE("Platform","Account")
# );
#
#
#
# """