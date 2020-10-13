from purbeurre import managers


class Product:
    """Describes a food product."""

    table = "product"

    def __init__(
        self, id=None, name=None, url=None, nutriscore=None, description=None
    ):
        """Builder.
        Args:
            id (int): product barcode
            name (str): full product name
            nutriscore (str): letter representing nutritional score
            url (str): url to the product page on the site used for the
            download.
            description (str): full product description
        """
        self.id = id
        self.name = name[:200]
        self.url = url
        self.nutriscore = nutriscore
        self.description = description

    def get_categories(self, order_by=None, limit=None):
        """Retrieves the categories associated with the product."""
        return Category.manager.get_categories_by_product(
            self, order_by=order_by, limit=limit
        )

    def get_stores(self, order_by=None, limit=None):
        """Retrieves the stores associated with the product."""
        return Product.manager.get_substitutes_by_product(
            self, order_by=order_by, limit=limit
        )

    def get_substitutes(self, order_by=None, limit=None):
        """Retrieves the substitutes associated with the product."""
        return Product.manager.get_substitutes_by_product(self)

    def get_products(self, order_by=None, limit=None):
        """Retrieves the products associated with the substitute."""
        return Product.manager.get_products_by_substitute(
            self, order_by=order_by, limit=limit
        )

    def add_categories(self, *categories):
        """Adds one or more categories to the product."""
        ProductCategory.manager.add_categories_to_product(self, *categories)

    def add_stores(self, *stores):
        """Adds one or more stores to the product."""
        ProductStore.manager.add_stores_to_product(self, *stores)

    def add_substitutes(self, *substitutes):
        """Registers substitutes associated with a product."""
        Favorite.manager.add_substitutes_to_product(self, *substitutes)

    def add_products(self, *products):
        """Registers products associated with a substitute."""
        Favorite.manager.add_products_to_substitute(self, *products)

    def __str__(self):
        """Returns a textual representation of the product."""
        return f"{self.name.capitalize()} ({self.nutriscore.upper()})"

    def format_info(self):
        return (
            f"Code: {self.id}\n"
            f"Nom: {self.name.capitalize()}\n"
            f"URL: {self.url}\n"
            f"Nutriscore: {self.nutriscore.upper()}\n"
            f"Description: {self.description}\n"
        )


class Category:
    """Description of product category within the food base."""

    table = "category"

    def __init__(self, id=None, name=None):
        """Builder.
        Args:
            id (int): unique and self-generated identifier for the category
            name (str): category name
        """
        self.id = id
        self.name = name[:100]

    def get_products(self, order_by=None, limit=None):
        """Retrieves the products associated with the category in the
        database."""
        return Product.manager.get_products_by_category(
            self, order_by=order_by, limit=limit
        )

    def add_products(self, *products):
        """Add one or more products to the category."""
        ProductCategory.manager.add_products_to_category(self, *products)

    def __str__(self):
        """Returns the textual representation of the category."""
        return f"{self.name}"


class Store:
    """Describes a store where products in the database can be
    be purchased.
    """

    table = "store"

    def __init__(self, id=None, name=None):
        """Builder.
        Args:
            id (int): unique and self-generated identifier for the store
            name (str): name of store
        """
        self.id = id
        self.name = name[:100]

    def get_products(self, order_by=None, limit=None):
        """Collects in base the products sold in this store."""
        return Product.manager.get_products_by_store(
            self, order_by=order_by, limit=limit
        )

    def add_products(self, *products):
        """Add one or more products to the store."""
        ProductStore.manager.add_products_to_store(self, *products)

    def __str__(self):
        """Returns the textual representation of a store."""
        return f"{self.name}"


class ProductCategory:
    """Describes an association between products and categories."""

    table = "product_category"

    def __init__(self, product=None, category=None):
        """Initialize a new association between product and category.
        Args:
            product (Product): instance of the product or its identifier
            category (Category): instance of the category or its identifier
        """
        self.product_id = (
            product.id if isinstance(product, Product) else product
        )
        self.category_id = (
            category.id if isinstance(category, Category) else category
        )


class ProductStore:
    """Describes an association between products and stores."""

    table = "product_store"

    def __init__(self, product=None, store=None):
        """Initializes a new association between product and store.
        Args:
            product (Product): instance of the product or its identifier
            store (Store): store instance or its identifier
        """
        self.product_id = (
            product.id if isinstance(product, Product) else product
        )
        self.store_id = store.id if isinstance(store, Store) else store


class Favorite:
    """Describes a recorded relationship between a product and its
    substitute."""

    table = "favorite"

    def __init__(
        self,
        product=None,
        substitute=None,
    ):
        """Initializes a new relationship between a product and its substitute.
        Args:
            product (Product): instance of the product or its identifier
            substitute (Product): substitute instance or its identifier
        """
        self.product_id = (
            product.id if isinstance(product, Product) else product
        )
        self.substitute_id = (
            substitute.id if isinstance(substitute, Product) else substitute
        )

    def get_product(self):
        """Retrieves the product associated with the favorite.""""
        return Product.manager.get_by_id(self.product_id)

    def get_substitute(self):
        """Retrieves the substitute associated with the favorite."""
        return Product.manager.get_by_id(self.substitute_id)

    def __str__(self):
        """Returns the textual representation of a favorite."""
        return (
            f"{self.get_product()} Can be replaced by "
            f"{self.get_substitute()}"
        )


# Definition of managers for each model
Product.manager = managers.ProductManager(Product)
Category.manager = managers.CategoryManager(Category)
Store.manager = managers.StoreManager(Store)
ProductCategory.manager = managers.ProductCategoryManager(ProductCategory)
ProductStore.manager = managers.ProductStoreManager(ProductStore)
Favorite.manager = managers.FavoriteManager(Favorite)
