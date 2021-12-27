import random
from db_api import *
import CustomExceptions
from aes import *
import string

def AddUserFromCMD():
    found = False
    while(not found):
        username = input("input a username:\n")
        if(not isUsernameUnique(username)):
            print("username already exists\n")
        else:
            found =True


    password = input("input password:\n") #TODO: add password restrictions to make it harder to crack

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

def generatePassword(userID,length,args):
    """
    c - capital letters
    s - special symbols
    n - numbers

    automaticly ignores anything else that is passed into the function
    """
    if(length<4 or length>64):
        raise ValueError("password length must be between 4 and 64")

    generated = False
    while not generated:
        #add character to make sure it is used in the password at least once
        characters = string.ascii_lowercase
        password += random.choice(characters)
        if('c' in args):
            characters += string.ascii_uppercase
            password += random.choice(characters)
        if('s' in args):
            characters+=string.punctuation
            password += random.choice(characters)
        if('n' in args):
            characters += string.digits
            password += random.choice(characters)

        password = ''.join(random.choice(characters) for i in range(length-len(password)))
        generated = isPasswordUnique(userID,password)
    return password

def isPasswordUnique(userID,password):
    """
    makes sure that the password is unique and not used in any other site
    """
    encrypted_passwords = getUserPasswords(userID)
    if(len(encrypted_passwords) == 0 ): #length of zero means there are no passwords so it is definatly unique
        return True

    cipher = AESCipher(str(userID))
    plain_passwords =[]
    for enc_password in encrypted_passwords:
        plain_passwords.append(cipher.decrypt(enc_password))

    if(password in plain_passwords):
        return False
    return True


def addLoginInfo(userID):
    """
    get site name, username and password and save to database
    site name needs to be unique
    can generate password based on given parameters (special characters, capital letters and digits)
    encrypts username and password before saving to database
    """
    #get the login info
    got_info=False
    while not got_info:
        site = input("name of the site:\r\n")
        if(not isSiteNameUnique(userID,site)):
            print("site name already exists")
        else:
            username = input("username:\r\n")
            action = input("would you like to generate a random password?(y/n) ")
            if(action =='y'):
                try: #generate random password
                    length = int(input("how many characters should the password have? "))
                    args = input("enter arguments for special characters (c - captial letters, n - numbers, s - special characters)\r\n")
                    password = generatePassword(userID,length,args)
                    got_info=True
                except ValueError as e:
                    print("please input a number between 4 and 64\r\n")
            else:
                password = input("password:\r\n")
                got_info=True

    if(not got_info): return

    #user confirmation to save the info
    answer = input("site name: %s\r\nusername: %s\r\npassword:%s\r\nare you sure you want to save?(y/n)\r\n" % (site,username,password))
    if(answer.lower() =='y'):
        #encrypt password and username
        cipher = AESCipher(str(userID))
        enc_username = cipher.encrypt(username)
        enc_password = cipher.encrypt(password)
        saveLoginInfo(userID,site,enc_username,enc_password)
        print("saved login info.\r\nreturning to menu\r\n")
    elif(answer.lower()=='n'): #if user as not confirmed saving can redo info input or go back to main menu
        answer = input("1 - input again\r\n2 - go back to menu\r\n")
        if(answer == '1'):
            addLoginInfo(userID)
        elif(answer =='2'):
            print("returning to menu\r\n\r\n")
    else:
        print("invalid answer")
        print("returning to menu\r\n\r\n")

def getLoginInfo(userID):
    """
    retrieve login info based on site name
    if site name is not in database returns list of similar site names
    """
    name = input("which site do you want to see?\r\n")
    try:
        loginInfo = retrieveLoginInfo(userID,name)
        cipher = AESCipher(str(userID))
        print("%s login info:\r\nusername: %s\r\npassword: %s\r\n" % (name,cipher.decrypt(loginInfo[0]),cipher.decrypt(loginInfo[1])))
    except CustomExceptions.MatchNotFound as e:
        print("could not find login info for site: %s" % (name))
        sites = fuzzyMatchSite(userID,name)
        if(len(sites) == 0):
            print("Could not find similar site names")
        else:
            print("Similar site names:")
            print(sites)


def updateLoginInfo(userID):
    """
    user can update one of the value fields of the site login info or generate a new password
    """
    site = input("what site login info would you like to update:")
    if(isSiteNameUnique(userID,site)):
        print("could not find site.\r\nsimilar site names:\r\n")
        print(fuzzyMatchSite(userID,site))
    else:
        action = input("what would you like to change?\r\n 1 - site name\r\n 2 - username\r\n 3 - password\r\n")
        #get plain text versions of username and password
        cipher = AESCipher(str(userID))
        enc = retrieveLoginInfo(userID,site)
        username = cipher.decrypt(enc[0])
        password = cipher.decrypt(enc[1])
        name = site

        #check user choice to update the relevent field
        if(action == '1'):
            name = input("what is the new name? ")
        elif(action =='2'):
            username = input("what is the new username? ")
        elif(action == '3'):
            action = input("would you like to generate a new password?(y/n) ")
            if(action.lower() == 'y'):
                got_pass = False
                while not got_pass:
                    try:
                        length = int(input("how many characters should the password have? "))
                        args = input("enter arguments for special characters (c - captial letters, n - numbers, s - special characters)\r\n")
                        password = generatePassword(userID,length,args)
                        got_pass = True
                    except ValueError as e:
                        print("please input a number between 4 and 64\r\n")
            elif(action.lower() == 'n'):
                password = input("what is the new password? ")
            else:
                print("invalid action\r\nreturning to menu\r\n\r\n")
                return None
        else:
            print("invalid action\r\nreturning to menu\r\n\r\n")
            return None

        print("new site login info:\r\n name: %s\r\n username: %s\r\n password: %s\r\n" %(name,username,password))
        answer = input("are you sure you would like to save this info?(y/n)") #user confirmation for saving new info
        if(answer.lower() =='y'):
            deleteLoginInfo(userID,site)
            saveLoginInfo(userID,name,cipher.encrypt(username),cipher.encrypt(password))
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
                print("logging out\r\n\r\n\r\n")
                main()
        else:
            print("invalid action - usersession")

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
        elif(action == '3'):
            quit()
        else:
            print("invalid option - main\r\n")


if __name__ == "__main__":
    main()
