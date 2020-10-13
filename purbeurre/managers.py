from purbeurre.database import db
from purbeurre import models


class BaseManager:
    """Manager at the base of the construction of all managers."""

    def __init__(self, modelname, tablename):
        """Initializes a new instance of BaseManager."""
        self._model = modelname
        self.table = tablename
        self.create_table()

    @property
    def model(self):
        """Model used by the manager."""
        if isinstance(self._model, str):
            self._model = getattr(models, self._model)
        return self._model

    def create(self, **kwargs):
        """Creates a new instance of the model from the arguments and
        saves the model.
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

    def get_all(self):
        """Retrieves all the instances of the model in the database."""
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {self.table}")
        results = [self.model(*row) for row in cursor]
        cursor.close()
        return results

    def get_by_id(self, id):
        """Retrieves an instance of the model in relation to its id."""
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
                id INT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                url VARCHAR(255) NOT NULL,
                nutriscore VARCHAR(1) NOT NULL,
                description TEXT
            )"""
        )
        cursor.close()

    def save(self, instance):
        """Save an instance of Product in the database."""
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


class ProductCategoryManager(BaseManager):
    """Manager responsible for managing the ProductCategory model."""

    def create_table(self):
        """Creates the association table associated with the
        ProductCategory model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                product_id INT,
                category_id INT,
                PRIMARY KEY(product_id, category_id),
                FOREIGN KEY (product_id) REFERENCES product(id),
                FOREIGN KEY (category_id) REFERENCES category(id)
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
        """Save a Store instance in database."""
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


class ProductStoreManager(BaseManager):
    """Manager responsible for managing the ProductStore model."""

    def create_table(self):
        """Creates the association table associated with the ProductStore model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                product_id INT,
                store_id INT,
                PRIMARY KEY(product_id, store_id),
                FOREIGN KEY (product_id) REFERENCES product(id),
                FOREIGN KEY (store_id) REFERENCES store(id)
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


class FavoriteManager(BaseManager):
    """Manager responsible for managing the Favorite model."""

    def create_table(self):
        """Creates the table associated with the Favorite model."""
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
                product_id INT,
                substitute_id INT,
                PRIMARY KEY(product_id, substitute_id),
                FOREIGN KEY (substitute_id) REFERENCES product(id),
                FOREIGN KEY (substitute_id) REFERENCES product(id)
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
