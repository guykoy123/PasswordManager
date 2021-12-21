import hashlib
import random
from db_api import *


def GenerateSaltedHash(str):
    saltValue = hex(random.randint(64,256))
    return  saltValue+hashlib.sha256((str+saltValue).encode()).hexdigest()


def CheckPass(password, storedHash):
    saltValue = storedHash[0:4]
    if(hashlib.sha256((password+saltValue).encode).hexdigest()==storedHash[4:]):
        return True
    return False

def main():
    TestDBConnection()

if __name__ == "__main__":
    main()
