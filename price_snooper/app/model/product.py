class Product:
    def __init__(self, product_url, product_name, category):
        self.created_at = None
        self.id = None
        self.product_url = product_url
        self.product_name = product_name
        self.category = category
        self.price_history = []

    def add_price_history(self, price):
        self.price_history.append(price)

    def __str__(self):
        return f"Product ID: {self.id}\nProduct Name: {self.product_name}\nProduct URL: {self.product_url}\nCreated Date: {self.created_at}\nCategory: {self.category}"

    def display_price_history(self):
        print("Price History:")
        for price in self.price_history:
            print(price)
