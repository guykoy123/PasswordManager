import sqlite3
import random
import re
import CustomExceptions
import hashlib
from fuzzywuzzy import fuzz

db_file = "database.db"
email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def GenerateSaltedHash(str):
    saltValue = hex(random.randint(64,256))
    return  saltValue[2:]+hashlib.sha256((str+saltValue[2:]).encode()).hexdigest()


def CheckPass(password, storedHash):
    saltValue = storedHash[0:2]
    if(hashlib.sha256((password+saltValue).encode()).hexdigest()==storedHash[2:]):
        return True
    return False

def userLogin(username,password):
    try:
        hash = getClientPassword(username)
        if(CheckPass(password,hash)):
            return getClientID(username)
        else:
            raise CustomExceptions.IncorrectLogin()
    except CustomExceptions.MatchNotFound as e:
        raise CustomExceptions.IncorrectLogin()


def getClientID(username):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor  = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = '%s'" % username)
        id = cursor.fetchall()[0][0]
        conn.close()
        return id
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def AddClient(name,password,email):
    foundID = False
    while (not foundID):
        id = random.randint(1000000,9999999)
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users VALUES ('%s','%s',%d,'%s')" % (name,password,id,email))
            conn.commit()

            foundID = True
        except sqlite3.Error as er:
            if("username" in str( (' '.join(er.args)))):
                raise CustomExceptions.NonUniqueValue('username')
            elif("email" in str( (' '.join(er.args)))):
                raise CustomExceptions.NonUniqueValue('email address')
        finally:
            conn.close()

def fuzzyMatchSite(userID, name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT site_name FROM Logins WHERE user_id = %d" % (userID))
        siteNames = cursor.fetchall()
        site_list =[]

    except sqlite3.Error as er:
        print(er)
    finally:
        if(conn):
            conn.close()
        for t in siteNames:
            if(fuzz.ratio(t[0],name)>=60):
                site_list.append(t[0])
        return site_list

def getUserPasswords(userID):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Logins WHERE user_id = %d" % (userID))
        passwords = cursor.fetchall()

    except sqlite3.Error as er:
        print(er)
    finally:
        conn.close()
        return passwords


def retrieveLoginInfo(userID,name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM Logins WHERE user_id = %d AND site_name = '%s'" % (userID,name))
        loginInfo = cursor.fetchall()

    except sqlite3.Error as er:
        print(er)
    finally:
        conn.close()
        if(len(loginInfo)==0):
            raise CustomExceptions.MatchNotFound("no site")
        return loginInfo[0]

def saveLoginInfo(userID,sitename,username,password):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Logins VALUES (%d,'%s','%s','%s')" % (userID,sitename,username,password))
        conn.commit()

    except sqlite3.Error as er:
        print(er)
    finally:
        conn.close()

def deleteLoginInfo(userID,sitename):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Logins WHERE user_id = %d AND site_name = '%s'" % (userID,sitename))
        conn.commit()

    except sqlite3.Error as er:
        print(er)
    finally:
        conn.close()

def isSiteNameUnique(userID,sitename):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT site_name FROM Logins WHERE user_id = %d AND site_name = '%s'" % (userID,sitename))
        t = cursor.fetchall()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        if(len(t)>0):
            return False
        else:
            return True

def isUsernameUnique(username):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = '%s'" % (username))
        users = cursor.fetchall()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        if(len(users)>0):
            return False
        else:
            return True

def isEmailUnique(email):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email = '%s'" % (email))
            emails = cursor.fetchall()

        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
            if(len(emails)>0):
                return False
            else:
                return True

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

def getClientPassword(username):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = '%s'" % (username))
            password = cursor.fetchall()
            if(len(password) == 1):
                return password[0][0]
            elif(len(password) > 1):
                raise Exception("Multiple Clients found with this username")
            else:
                raise CustomExceptions.MatchNotFound(username)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

def main():
    TestDBConnection()



if __name__ == '__main__':
    main()
