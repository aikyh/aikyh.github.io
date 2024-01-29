import shelve


class Cart:
    def __init__(self):
        self.carts = shelve.open('carts.db', writeback=True)
        self.items = {}

    def save_cart(self, id):
        self.carts[id] = self.items

    def get_cart(self):
        return self.carts['1']

    def add_item(self, id, product):
        if '1' in self.carts:
            items = self.carts[id]
            if product.name in items:
                items[product.name]['quantity'] += 1
            else:
                items[product.name] = {'product': product, 'quantity': 1}
            print(items)
            self.carts[id] = items
        else:
            items[product.name] = {'product': product, 'quantity': 1}
            self.carts[id] = items

    def remove_item(self, id, product):
        items = self.carts[id]
        if product.name in items:
            if items[product.name]['quantity'] > 1:
                items[product.name]['quantity'] -= 1
            else:
                del items[product.name]
        self.carts[id] = items

    def get_items(self):
        return list(self.items.values())

    def clear(self):
        self.items = {}

    def close(self):
        self.carts.close()
