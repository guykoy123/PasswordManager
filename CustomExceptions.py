class MatchNotFound(Exception):
    def __init__(self,username, message='No client with username: '):
        self.username = username
        self.message = message
        # Call the base class constructor with the parameters it needs
        super(MatchNotFound, self).__init__(message + username)


    def __str__(self):
        return self.message + self.username


class IncorrectLogin(Exception):
    def __init__(self, message='username or password is incorrect, please try again'):
        self.message = message
        # Call the base class constructor with the parameters it needs
        super(IncorrectLogin, self).__init__(message)


    def __str__(self):
        return self.message


class NonUniqueValue(Exception):
    def __init__(self, value, message=' already exists'):
        self.value = value
        self.message = message
        # Call the base class constructor with the parameters it needs
        super(NonUniqueValue, self).__init__(value + message)


    def __str__(self):
        return self.value + self.message
