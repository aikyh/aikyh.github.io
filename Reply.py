class Reply:
    count_id = 0

    def __init__(self, customer_name, product_name, email, reply_date, comments):
        Reply.count_id += 1
        self.__reply_id = Reply.count_id
        self.__email = email
        self.__customer_name = customer_name
        self.__product_name = product_name
        self.__reply_date = reply_date
        self.__comments = comments

    # accessor methods
    def get_reply_id(self):
        return self.__reply_id

    def get_email(self):
        return self.__email

    def get_customer_name(self):
        return self.__customer_name

    def get_product_name(self):
        return self.__product_name


    def get_reply_date(self):
        return self.__reply_date

    def get_comments(self):
        return self.__comments

    # mutator methods
    def set_reply_id(self, reply_id):
        self.__reply_id = reply_id

    def set_email(self, email):
        self.__email = email

    def set_customer_name(self, customer):
        self.__customer_name = customer

    def set_product_name(self, product_name):
        self.__product_name = product_name


    def set_reply_date(self, reply_date):
        self.__reply_date = reply_date

    def set_comments(self, comments):
        self.__comments = comments

