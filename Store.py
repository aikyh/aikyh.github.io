import shelve


class Store:
    def __init__(self):
        self.products = shelve.open('products.db', writeback=True)

    def add_product(self, product):
        self.products[product.name] = product

    def get_product(self, name):
        print(self.products.get(name))
        return self.products.get(name)

    def get_all_products(self):
        return list(self.products.values())

    def close(self):
        self.products.close()

