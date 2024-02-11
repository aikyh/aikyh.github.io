class Product:
    count_id = 0

    def _init_(self, name, price, description, tags):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__tags = tags

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_tags(self):
        return self.__tags

    def set_tags(self, tags):
        self.__tags = tags