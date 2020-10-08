
class Product:
    """Describes a food product."""

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

    def __init__(self, id=None, name=None):
        """Builder.
         Args:
             id (int): unique and auto-generated identifier for the store
             name (str): store name
        """
        self.id = id
        self.name = name
