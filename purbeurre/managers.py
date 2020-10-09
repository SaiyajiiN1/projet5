from purbeurre.database import db
from purbeurre.models import Product, Category, Store


class BaseManager:
    """Manager at the base of the construction of all managers."""

    def __init__(self, model, tablename):
        self._model = model
        self._tablename = tablename
        self.create_table()


class ProductManager(BaseManager):

    def create_table(self):
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tablename} (
                id INT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                url VARCHAR(255) NOT NULL,
                nutriscore VARCHAR(1) NOT NULL,
                description TEXT
            )"""
        )
        cursor.close()


class CategoryManager(BaseManager):

    def create_table(self):
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tablename} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """
        )


class ProductCategoryManager(BaseManager):

    def create_table(self):
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tablename} (
                product_id INT,
                category_id INT,
                PRIMARY KEY(product_id, category_id),
                FOREIGN KEY (product_id) REFERENCES product(id),
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
            """
        )


class StoreManager(BaseManager):

    def create_table(self):
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tablename} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """
        )


class ProductStoreManager(BaseManager):

    def create_table(self):
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tablename} (
                product_id INT,
                store_id INT,
                PRIMARY KEY(product_id, store_id),
                FOREIGN KEY (product_id) REFERENCES product(id),
                FOREIGN KEY (store_id) REFERENCES store(id)
            )
            """
        )


products = ProductManager(Product, "product")
categories = CategoryManager(Category, "category")
stores = CategoryManager(Store, "store")
product_category_set = ProductCategoryManager(None, "product_category")
store_category_set = ProductStoreManager(None, "product_store")
