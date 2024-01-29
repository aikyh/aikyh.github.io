class Review:
    count_id = 0

    def __init__(self, customer_name, product_name, rating, email, review_date, comments):
        Review.count_id += 1
        self.__review_id = Review.count_id
        self.__email = email
        self.__customer_name = customer_name
        self.__product_name = product_name
        self.__rating = rating
        self.__review_date = review_date
        self.__comments = comments

    # accessor methods
    def get_review_id(self):
        return self.__review_id

    def get_email(self):
        return self.__email

    def get_customer_name(self):
        return self.__customer_name

    def get_product_name(self):
        return self.__product_name

    def get_rating(self):
        return self.__rating

    def get_review_date(self):
        return self.__review_date

    def get_comments(self):
        return self.__comments

    # mutator methods
    def set_review_id(self, review_id):
        self.__review_id = review_id

    def set_email(self, email):
        self.__email = email

    def set_customer_name(self, customer):
        self.__customer_name = customer

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_rating(self, rating):
        self.__rating = rating

    def set_review_date(self, review_date):
        self.__review_date = review_date

    def set_comments(self, comments):
        self.__comments = comments

