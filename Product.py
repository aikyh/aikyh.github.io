class Product:
    count_id = 0

    def __init__(self, name, price, image):
        Product.count_id += 1
        self.name = name
        self.price = price
        self.image = image
