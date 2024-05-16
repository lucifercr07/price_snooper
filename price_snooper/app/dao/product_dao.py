from app.utils.db_utils import DatabaseUtil


class ProductDAO:
    def __init__(self, db_name):
        self.db_utils = DatabaseUtil(db_name)

    def insert_product(self, product):
        query = """
            INSERT INTO products (product_name, product_url, created_at, category)
            VALUES (?, ?, ?, ?)
        """
        params = (product.product_name, product.product_url, product.created_at, product.category)
        return self.db_utils.execute(query, params)

    def close(self):
        self.db_utils.close()
