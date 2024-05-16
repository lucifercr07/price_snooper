import datetime

from app.utils.db_utils import DatabaseUtil


class PriceHistoryDao:
    def __init__(self, db_name):
        self.db_utils = DatabaseUtil(db_name)

    def insert_price_history(self, price_history):
        query = """
            INSERT INTO price_history (product_id, lowest_price, current_price, expected_discount, currency, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (price_history.product_id, price_history.lowest_price, price_history.current_price, price_history.expected_discount, price_history.currency, datetime.datetime.utcnow())
        return self.db_utils.execute(query, params)

    def close(self):
        self.db_utils.close()
