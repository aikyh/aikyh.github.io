class CheckIn:
    count_id = 0

    # initializer method
    def __init__(self, name, email):
        CheckIn.count_id += 1
        self.__CheckIn_id = CheckIn.count_id
        self.__name = name
        self.__email = email

    # accessor methods
    def get_checkin_id(self):
        return self.__CheckIn_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    # mutator methods
    def set_checkin_id(self, CheckIn):
        self.__CheckIn_id = CheckIn

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email
