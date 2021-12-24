import random
from db_api import *
import CustomExceptions

def AddUserFromCMD():
    found = False
    while(not found):
        username = input("input a username:\n")
        if(not isUsernameUnique(username)):
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
            if(not isEmailUnique(email)):
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

def getSimilarSitesInfo(userID,name):
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
        getSimilarSitesInfo(userID,name)

def updateLoginInfo(userID):
    site = input("what site login info would you like to update:")
    if(isSiteNameUnique(userID,site)):
        print("could not find site.\r\nsimilar site names:\r\n")
        print(fuzzyMatchSite(userID,site))
    else:
        action = input("what would you like to change?\r\n 1 - site name\r\n 2 - username\r\n 3 - password\r\n")
        username,password = retrieveLoginInfo(userID,site)
        name = site
        if(action == '1'):
            name = input("what is the new name? ")
        elif(action =='2'):
            username = input("what is the new username? ")
        elif(action == '3'):
            password = input("what is the new password? ")
        else:
            print("invalid action\r\nreturning to menu\r\n\r\n")
            return None

        print("new site login info:\r\n name: %s\r\n username: %s\r\n password: %s\r\n" %(name,username,password))
        answer = input("are you sure you would like to save this info?(y/n)")
        if(answer.lower() =='y'):
            deleteLoginInfo(userID,site)
            saveLoginInfo(userID,name,username,password)
            print("Login info saved\r\n")
        else:
            print("returning to menu\r\n\r\n")


def deleteSite(userID):
    site = input("what site login info would you like to delete:")
    if(isSiteNameUnique(userID,site)):
        print("could not find site.\r\nsimilar site names:\r\n")
        print(fuzzyMatchSite(userID,site))
    else:
        answer = input("are you sure you would like to delete the login info for %s? (y/n)" % (site))
        if(answer.lower() == 'y'):
            deleteLoginInfo(userID,site)
            print("delete login info for %s\r\n" % site)
        else:
            print("returning to menu\r\n\r\n")

def userSession(username,userID):
    print("\r\nlogged in as "+username +"\r\n")
    while (True):
        action = input("1 - get login info\r\n2 - add login info\r\n3 - update login info\r\n4 - delete login info\r\n5 - logout\r\n")
        if(action == '1'):
            getLoginInfo(userID)
        elif(action == '2'):
            addLoginInfo(userID)
        elif(action == '3'):
            updateLoginInfo(userID)
        elif(action == '4'):
            deleteSite(userID)
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
        action = input("1 - login \r\n2 - add user\r\n3 - quit\r\n")
        if(action == '1'):
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
        elif(action == '2'):
            AddUserFromCMD()
        if(action == '3'):
            quit()
        else:
            print("invalid option\r\n")


if __name__ == "__main__":
    main()
