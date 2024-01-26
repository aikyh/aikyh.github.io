import shelve


class Company:
    count_id = 0

    def __init__(self, company_name, email, date_joined, address, password):
        Company.count_id += 1
        self.__company_id = Company.count_id
        self.__company_name = company_name
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address
        self.__password = password

    def get_company_id(self):
        return self.__company_id

    def set_company_id(self, company_id):
        self.__company_id = company_id

    def get_company_name(self):
        return self.__company_name

    def set_company_name(self, company_name):
        self.__company_name = company_name

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_date_joined(self):
        return self.__date_joined

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

