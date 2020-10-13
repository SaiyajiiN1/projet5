from purbeurre import managers


class Product:
    """Describes a food product."""

    manager = managers.ProductManager("Product", "product")

    def __init__(
        self, id=None, name=None, nutriscore=None, url=None, description=None
    ):
        """Builder.
         Args:
             id (int): barcode of the product
             name (str): full name of the product
             nutriscore (str): letter representing the nutritional score
             url (str): url to the product page on the site used for the
             download.
             description (str): full description of the product
        """
        self.id = id
        self.name = name
        self.nutriscore = nutriscore
        self.url = url
        self.description = description


class Category:
    """Description of product category within the food base."""

    manager = managers.CategoryManager("Category", "category")

    def __init__(self, id=None, name=None):
        """Builder.
         Args:
             id (int): unique and auto-generated identifier for the category
             name (str): name of the category
        """
        self.id = id
        self.name = name


class Store:
    """Describes a store in which database products can be purchased.
    """

    manager = managers.StoreManager("Store", "store")

    def __init__(self, id=None, name=None):
        """Builder.
         Args:
             id (int): unique and auto-generated identifier for the store
             name (str): store name
        """
        self.id = id
        self.name = name


class ProductCategory:
    """Describes an association between products and categories."""

    manager = managers.ProductCategoryManager(
        "ProductCategory", "product_category"
    )

    def __init__(self, product_id, category_id):
        """Initialise une nouvelle association entre produit et catégorie.
        Args:
            product_id (int): product id
            category_id (int): category id
        """
        self.product_id = product_id
        self.category_id = category_id


class ProductStore:
    """Describes an association between products and stores."""

    manager = managers.ProductStoreManager("ProductStore", "product_store")

    def __init__(self, product_id, store_id):
        """Initialise une nouvelle association entre produit et magasin.
        Args:
            product_id (int): product id
            store_id (int): store id
        """
        self.product_id = product_id
        self.store_id = store_id


class Favorite:
    """Describes a recorded relationship between a product and its substitute."""

    manager = managers.FavoriteManager("Favorite", "favorite")

    def __init__(self, product_id, substitute_id):
        """Initializes a new relationship between a product and its substitute.
        Args:
            product_id (int): product id
            substitute_id (int): healthier substitute identifier
        """
        self.product_id = product_id
        self.substitute_id = substitute_id
