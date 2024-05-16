class PriceHistory:
    def __init__(self, product_id, lowest_price, current_price, currency, expected_discount=None):
        self.id = None
        self.product_id = product_id
        self.lowest_price = lowest_price
        self.current_price = current_price
        self.expected_discount = expected_discount
        self.currency = currency
        self.updated_at = None
        self.created_at = None

    def __str__(self):
        return f"Price ID: {self.id}\nInitial Price: {self.initial_price}\nCurrent Price: {self.current_price}\nExpected Discount: {self.expected_discount}\nUpdated Date: {self.updated_at}\nCurrency: {self.currency}"
