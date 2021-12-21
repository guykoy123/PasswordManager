import random
from db_api import *
import CustomExceptions

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

    AddClient(username,GenerateSaltedHash(password),email)

def addLoginInfo(userID):
    while True:
        site = input("name of the site:\r\n")
        if(isSiteNameUnique(userID,site)):
            username = input("username:\r\n")
            password = input("password:\r\n")
            answer = input("site name: %s\r\nusername: %s\r\npassword:%s\r\nare you sure you want to save?(y/n)\r\n" % (site,username,password))
            if(answer.lower() =='y'):
                saveLoginInfo(userID,site,username,password)
                print("saved login info.\r\nreturning to menu\r\n")
                break
        else:
            print("site name already exists")

def userSession(username,userID):
    print("\r\nlogged in as "+username +"\r\n")
    while (True):
        action = input("1 - check login info\r\n2 - add login info\r\n3 - update login info\r\n4 - delete login info\r\n5 - logout\r\n")
        if(action == '1'):
            pass
        elif(action == '2'):
            addLoginInfo(userID)
        elif(action == '3'):
            pass
        elif(action == '4'):
            pass
        elif(action == '5'):
            a = input("are you sure you want to logout?(y/n) ")
            if(a.lower() == 'y'):
                print("loggin out")
                main()
        else:
            print("invalid action")

def main():
    TestDBConnection()
    while (True):
        action = input("1 - add user \r\n2 - login\r\n")
        if(action == '1'):
            AddUserFromCMD()
        if(action == '2'):
            try:
                username = input("username: ")
                password = input("password: ")
                userID = userLogin(username,password)
                if(userID):
                    print("login successful, "+str(userID))
                    userSession(username,userID)
            except CustomExceptions.IncorrectLogin as e:
                print(e)
            except Exception as e:
                print("main: " +str(e))


if __name__ == "__main__":
    main()
