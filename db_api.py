import sqlite3
import random
import re
db_file = "database.db"
email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def AddClient(name,password,email):
    foundID = False
    while (not foundID):
        id = random.randint(1000000,9999999)
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Clients VALUES ('%s','%s',%d,'%s')" % (name,password,id,email))
            conn.commit()

            foundID = True
        except sqlite3.Error as er:
            if("username" in str( (' '.join(er.args)))):
                print("username is not UNIQUE")
                foundID = True
            elif("email" in str( (' '.join(er.args)))):
                print("email is not UNIQUE")
                foundID = True
        finally:
            conn.close()

def isUsernameUnique(username):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Clients WHERE username = '%s'" % (username))
        users = cursor.fetchall()
        if(len(users)>0):
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def isEmailUnique(email):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM Clients WHERE email = '%s'" % (email))
            emails = cursor.fetchall()
            if(len(emails)>0):
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

def TestDBConnection():
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("connected to db successfully")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

def AddUserFromCMD():
    found = False
    while(not found):
        username = input("input a username:\n")
        if(isUsernameUnique(username)):
            print("username already exists\n")
        else:
            found =True


    password = input("input password:\n")

    found = False
    while(not found):
        email = input("input email:\n").lower() #email is allways small cap letters
        if(not re.match(email_regex,email)):
            print("invalid email address")
        else:
            if(isEmailUnique(email)):
                print("email already exists\n")
            else:
                found =True

    AddClient(username,password,email)

def main():
    TestDBConnection()
    while (True):
        AddUserFromCMD()

if __name__ == '__main__':
    main()
