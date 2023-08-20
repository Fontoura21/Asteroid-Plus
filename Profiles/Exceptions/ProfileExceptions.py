class NameWithSpace(Exception):
    def __init__(self):
        message = "Name can not have Spaces"
        super().__init__(message)

class NameWithMoreThan5Letters(Exception):
    def __init__(self):
        message = "Name can not have more than 5 letters"
        super().__init__(message)

class NullName(Exception):
    def __init__(self):
        message = "Name can not be null"
        super().__init__(message)

class ProfileAlreadyExist(Exception):
    def __init__(self):
        message = "Profile Already Exist"
        super().__init__(message)