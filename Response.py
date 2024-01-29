class Response:
    count_id = 0

    def __init__(self, fname, lname, phone, email, add1, add2, pcode, dmethod, amount):
        Response.count_id += 1
        self.__response_id = Response.count_id
        self.__fname = fname
        self.__lname = lname
        self.__phone = phone
        self.__email = email
        self.__add1 = add1
        self.__add2 = add2
        self.__pcode = pcode
        self.__dmethod = dmethod
        self.__amount = amount

    def get_response_id(self):
        return self.__response_id

    def set_response_id(self, response_id):
        self.__response_id = response_id

    def get_fname(self):
        return self.__fname

    def set_fname(self, fname):
        self.__fname = fname

    def get_lname(self):
        return self.__lname

    def set_lname(self, lname):
        self.__lname = lname

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_add1(self):
        return self.__add1

    def set_add1(self, add1):
        self.__add1 = add1

    def get_add2(self):
        return self.__add2

    def set_add2(self, add2):
        self.__add2 = add2

    def get_pcode(self):
        return self.__pcode

    def set_pcode(self, pcode):
        self.__pcode = pcode

    def get_dmethod(self):
        return self.__dmethod

    def set_dmethod(self, dmethod):
        self.__dmethod = dmethod

    def get_amount(self):
        return self.__amount

    def set_amount(self, amount):
        self.__amount = amount
