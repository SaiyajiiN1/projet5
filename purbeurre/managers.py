from purbeurre.database import db, register_manager
from purbeurre import models


class BaseManager:
    """Manager at the base of the construction of all managers."""

    def __init__(self, model):
        """Initialise une nouvelle instance de BaseManager."""
        self.model = model
        self.table = model.table
        register_manager(self)

    def create(self, **kwargs):
        """Create a new instance of the model from the arguments and
        save the model.
        """
        instance = self.model(**kwargs)
        self.save(instance)
        return instance

    def delete_all(self):
        """Clears all items from the table."""
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {self.table}")
        db.commit()
        cursor.close()

    def drop_table(self):
        """Delete your table itself."""
        cursor = db.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.table}")
        db.commit()
        cursor.close()

    def _format_order_by(self, order_by):
        if not isinstance(order_by, list) or not order_by:
            return ""
        else:
            limit = [str(number) for number in limit]
            return f" ORDER BY {', '.join(order_by)}"

    def _format_limit(self, limit):
        if not isinstance(limit, list) or not limit:
            return ""
        else:
            return f" LIMIT {', '.join(limit)}"

    def get_all(self, order_by=None, limit=None):
        """Retrieves all the instances of the model in the database."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM {self.table}"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}"
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results

    def get_by_id(self, id):
        """Retrieves in base an instance of the model compared to its id."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM {self.table} WHERE id = %(id)s", {"id": id}
        )
        results = [self.model(*row) for row in cursor]
        if len(results) == 0:
            raise ValueError(f"No instance corresponds to id = {id}")
        cursor.close()
        return results[0]


class ProductManager(BaseManager):
    """Manager responsible for managing the Product model."""

    def create_table(self):
        """Creates the table associated with the Product model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                id BIGINT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                url VARCHAR(255) NOT NULL,
                nutriscore VARCHAR(1) NOT NULL,
                description TEXT
            )"""
        )
        cursor.close()

    def save(self, instance):
        """Save an instance of Product in database."""
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table} (
                id, name, url, nutriscore, description
            )
            VALUES (%(id)s, %(name)s, %(url)s, %(nutriscore)s, %(description)s)
            """,
            vars(instance),
        )
        db.commit()
        cursor.close()

    def get_products_by_category(self, category, order_by=None, limit=None):
        """Retrieves all the products associated with a category in the
        database."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, name, url, nutriscore, description "
            f"FROM {self.table} "
            f"JOIN {models.ProductCategory.table} "
            f"    ON {self.table}_id = id "
            f"WHERE {models.Category.table}_id = %(id)s"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}",
            vars(category),
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results

    def get_products_by_store(self, store, order_by=None, limit=None):
        """Retrieves all the products associated with a store in the
        database."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, name, url, nutriscore, description "
            f"FROM {self.table} "
            f"JOIN {models.ProductStore.table} "
            f"    ON {self.table}_id = id "
            f"WHERE {models.Store.table}_id = %(id)s"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}",
            vars(store),
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results

    def get_substitutes_by_product(self, product, order_by=None, limit=None):
        """Retrieves all the substitutes associated with a product in the
        database."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, name, url, nutriscore, description "
            f"FROM {self.table} "
            f"JOIN {models.Favorite.table} "
            f"    ON substitute_id = id "
            f"WHERE {models.Product.table}_id = %(id)s"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}",
            vars(product),
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results

    def get_products_by_substitute(
        self, substitute, order_by=None, limit=None
    ):
        """Retrieves in base all the products associated with a product as
        that substitute.
        """
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, name, url, nutriscore, description "
            f"FROM {self.table} "
            f"JOIN {models.Favorite.table}  "
            f"    ON {self.table}_id = id "
            f"WHERE substitute_id = %(id)s"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}",
            vars(substitute),
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results


class CategoryManager(BaseManager):
    """Manager responsible for managing the Category model."""

    def create_table(self):
        """Creates the table associated with the Category model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """
        )
        cursor.close()

    def save(self, instance):
        """Save an instance of Category in database."""
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table} (id, name)
            VALUES (%(id)s, %(name)s)
            ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
            """,
            vars(instance),
        )
        instance.id = cursor.lastrowid
        db.commit()
        cursor.close()

    def get_categories_by_product(self, product, order_by=None, limit=None):
        """Retrieves all the categories associated with a product in the
        database."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, name "
            f"FROM {self.table} "
            f"JOIN {models.ProductCategory.table} "
            f"    ON {self.table}_id = id "
            f"WHERE {models.Product.table}_id = %(id)s"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}",
            vars(product),
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results


class ProductCategoryManager(BaseManager):
    """Manager responsible for managing the ProductCategory model."""

    def create_table(self):
        """Creates the association table associated with the ProductCategory
        model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                {models.Product.table}_id BIGINT,
                {models.Category.table}_id INT,
                PRIMARY KEY({models.Product.table}_id, category_id),
                FOREIGN KEY ({models.Product.table}_id)
                    REFERENCES {models.Product.table}(id),
                FOREIGN KEY ({models.Category.table}_id)
                    REFERENCES {models.Category.table}(id)
            )
            """
        )
        cursor.close()

    def save(self, instance):
        """Save an instance of ProductCategory in database."""
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table} (product_id, category_id)
            VALUES (%(product_id)s, %(category_id)s)
            """,
            vars(instance),
        )
        db.commit()
        cursor.close()

    def get_by_id(self, product_id, category_id):
        raise NotImplementedError(
            "get_by_id() is not supported on ProductCategory"
        )

    def add_categories_to_product(self, product, *categories):
        """Add categories to a product."""
        for category in categories:
            self.create(product=product, category=category)

    def add_products_to_category(self, category, *products):
        """Adds products to a category."""
        for product in products:
            self.create(product=product, category=category)


class StoreManager(BaseManager):
    """Manager responsible for managing the Store model."""

    def create_table(self):
        """Creates the table associated with the Store model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE
            )
            """
        )
        cursor.close()

    def save(self, instance):
        """Save a Store instance in the database."""
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table} (id, name)
            VALUES (%(id)s, %(name)s)
            ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
            """,
            vars(instance),
        )
        instance.id = cursor.lastrowid
        db.commit()
        cursor.close()

    def get_stores_by_product(self, product, order_by=None, limit=None):
        """Retrieves all the stores associated with a product in the
        database."""
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, name "
            f"FROM {self.table} "
            f"JOIN {models.ProductStore.table} "
            f"    ON {self.table}_id = id "
            f"WHERE {models.Product.table}_id = %(id)s"
            f"{self._format_order_by(order_by)}"
            f"{self._format_limit(limit)}",
            vars(product),
        )
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results


class ProductStoreManager(BaseManager):
    """Manager responsible for managing the ProductStore model."""

    def create_table(self):
        """Creates the association table associated with the
        ProductStore model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                {models.Product.table}_id BIGINT,
                {models.Store.table}_id INT,
                PRIMARY KEY({models.Product.table}_id, store_id),
                FOREIGN KEY ({models.Product.table}_id)
                    REFERENCES {models.Product.table}(id),
                FOREIGN KEY ({models.Store.table}_id)
                    REFERENCES {models.Store.table}(id)
            )
            """
        )
        cursor.close()

    def save(self, instance):
        """Save an instance of ProductStore in database."""
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table} (product_id, store_id)
            VALUES (%(product_id)s, %(store_id)s)
            """,
            vars(instance),
        )
        db.commit()
        cursor.close()

    def get_by_id(self, product_id, category_id):
        raise NotImplementedError(
            "get_by_id() is not supported on ProductStore"
        )

    def add_stores_to_product(self, product, *stores):
        """Adds stores to a product."""
        for store in stores:
            self.create(product=product, store=store)

    def add_products_to_store(self, store, *products):
        """Adds products to a store."""
        for product in products:
            self.create(product=product, store=store)


class FavoriteManager(BaseManager):
    """Manager responsible for managing the Favorite model."""

    def create_table(self):
        """Creates the table associated with the Favorite model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                {models.Product.table}_id BIGINT,
                substitute_id BIGINT,
                PRIMARY KEY({models.Product.table}_id, substitute_id),
                FOREIGN KEY ({models.Product.table}_id)
                    REFERENCES {models.Product.table}(id),
                FOREIGN KEY (substitute_id)
                    REFERENCES {models.Product.table}(id)
            )
            """
        )
        cursor.close()

    def save(self, instance):
        """Save an instance of Favorite in the database."""
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {self.table} (product_id, substitute_id)
            VALUES (%(product_id)s, %(substitute_id)s)
            """,
            vars(instance),
        )
        db.commit()
        cursor.close()

    def get_by_id(self, product_id, category_id):
        raise NotImplementedError("get_by_id() is not supported on Favorite")

    def add_products_to_substitute(self, substitute, *products):
        """Adds products to a substitute."""
        for product in products:
            self.create(product=product, substitute=substitute)

    def add_substitutes_to_product(self, product, *substitutes):
        """Adds substitutes to a product."""
        for substitute in substitutes:
            self.create(product=product, substitute=substitute)
