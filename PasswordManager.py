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
            elif(answer.lower()=='n'):
                answer = input("1 - input again\r\n2 - go back to menu\r\n")
                if(answer == '1'):
                    pass
                elif(answer =='2'):
                    print("returning to menu\r\n\r\n")
                    break
                else:
                    print("invalid answer")
                    print("returning to menu\r\n\r\n")
                    break
        else:
            print("site name already exists")

def getSimilarSites(userID,name):
    print("similar site:\r\n")
    similarSites = fuzzyMatchSite(userID,name)
    if(len(similarSites)>0):
        i=1
        for s in similarSites:
            print("%d - %s\r\n" % (i,s))
            i+=1
        action = input("would you like to see one of these site? (if not press b)\r\n")
        if(action == 'b'):
            print("returning to menu\r\n\r\n")
        else:
            try:
                i = int(action)
                print("retrieving login info for %s:\r\n" % (similarSites[i-1]))
                loginInfo = retrieveLoginInfo(userID,similarSites[i-1])
                print("nusername: %s\r\npassword: %s\r\n" % (loginInfo[0],loginInfo[1]))
            except Exception as e:
                print(e)
                print("invalid action, returning to menu\r\n\r\n")
    else:
        print("could not find similar sites\r\n")

def getLoginInfo(userID):
    name = input("which site do you want to see?\r\n")
    try:
        loginInfo = retrieveLoginInfo(userID,name)
        print("%s login info:\r\nusername: %s\r\npassword: %s\r\n" % (name,loginInfo[0],loginInfo[1]))
    except CustomExceptions.MatchNotFound as e:
        print("could not find login info for site: %s\r\n" % (name))
        getSimilarSites(userID,name)

def userSession(username,userID):
    print("\r\nlogged in as "+username +"\r\n")
    while (True):
        action = input("1 - get login info\r\n2 - add login info\r\n3 - update login info\r\n4 - delete login info\r\n5 - logout\r\n")
        if(action == '1'):
            getLoginInfo(userID)
        elif(action == '2'):
            addLoginInfo(userID)
        elif(action == '3'):
            print("option has not been implemented yet")
        elif(action == '4'):
            print("option has not been implemented yet")
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
        action = input("1 - add user \r\n2 - login\r\n3 - quit\r\n")
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
        if(action == '3'):
            quit()
        else:
            print("invalid option\r\n")


if __name__ == "__main__":
    main()
