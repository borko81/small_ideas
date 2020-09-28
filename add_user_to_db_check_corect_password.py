import hashlib
import sqlite3
import os

# PATH TO DB
FILE_PATH = os.path.join(os.getcwd(), 'users.db')

create_table_sql = """ CREATE TABLE IF NOT EXISTS USERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name CHAR(20) NOT NULL,
    password CHAR(64) NOT NULL
);"""


class User:
    ''' Check password in hex'''

    def hex_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password, user_password):
        check = self.hex_password(password)
        return check == user_password


class UsrInitialize(User):
    ''' User initializer'''

    def __init__(self, name, password):
        self.name = name
        self.password = self.hex_password(password)

    def return_data(self):
        return self.name, self.password


# DB Classe's
class DB:
    ''' For create conn and db'''
    @staticmethod
    def create_database():
        try:
            conn = sqlite3.connect(FILE_PATH)
        except sqlite3.Error as e:
            print(e)
        else:
            return conn


class CreateTable(DB):
    '''For create table'''
    @staticmethod
    def create_table():
        conn = DB.create_database()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(create_table_sql)
            except sqlite3.Error as e:
                print(e)


class InsertUserInfo(DB):
    '''For insert user info into table'''
    @staticmethod
    def insert_data(data):
        conn = DB.create_database()
        name, password = data
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(
                    '''
                    INSERT INTO USERS (name, password) VALUES (
                        ?, ?   
                    )''', (name, password, )
                )
                conn.commit()
            except sqlite3.Error as e:
                print(e)

    @staticmethod
    def get_data(username):
        conn = DB.create_database()
        if conn is not None:
            try:
                cur = conn.cursor()
                name = cur.execute(
                    '''SELECT password from users where name = ?''', (username, )
                )
            except sqlite3.Error as e:
                print(e)
            else:
                return name.fetchone()[0]


def main():
    print('''
    1 (for insert user)
    2 (for check password)
    3 (for create table)
    ''')
    c = int(input('Enter your choice :'))

    def create_user():
        name = input("Enter username :")
        password = input("Enter password :")
        test = UsrInitialize(name, password)
        data = test.return_data()
        InsertUserInfo.insert_data(data)
        print("Status OK")

    def check_db_password():
        name = input("Enter username :")
        password = input("Enter password :")
        db_pass = InsertUserInfo.get_data(name)
        test = User()
        result = test.check_password(password, db_pass)
        print(result)
        return result

    choice = {
        1: create_user,
        2: check_db_password,
        3: CreateTable.create_table,
    }
    try:
        magic = choice[c]
    except KeyError as e:
        print(f"{c} is not valid input")
    else:
        return choice.get(c)()


if __name__ == '__main__':
    main()
