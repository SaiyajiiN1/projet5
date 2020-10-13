"""Script managing the creation and filling of the database."""

from settings import PRODUCT_CLIENT_PAGE_SIZE, PRODUCT_CLIENT_NUMBER_OF_PAGES
from purbeurre.database import create_tables
from purbeurre.apiclients import OpenfoodfactsClient
from purbeurre.validators import ProductValidator
from purbeurre.normalizers import ProductNormalizer
from purbeurre.models import Product, Category, Store


def main():
    """Primary entry point for the installation script."""
    # We instantiate the necessary objects
    client = OpenfoodfactsClient()
    validator = ProductValidator()
    normalizer = ProductNormalizer()

    # Download data from openfoodfacts
    products = client.get_products_by_popularity(
        page_size=PRODUCT_CLIENT_PAGE_SIZE,
        number_of_pages=PRODUCT_CLIENT_NUMBER_OF_PAGES,
    )
    # Validate the received data
    products = validator.filter(products)
    # Normalize received data
    normalizer.normalize_all(products)

    # Create the database tables
    create_tables()
    # Fill the database
    for product_info in products:
        # Retrieving categories and stores
        categories = product_info.pop("categories")
        stores = product_info.pop("stores")

        # Registration of product
        product = Product.manager.create(**product_info)

        # Creation of categories and association with the product
        for category_name in categories:
            category = Category.manager.create(name=category_name)
            product.add_categories(category)

        # Creation of stores and association with the product
        for store_name in stores:
            store = Store.manager.create(name=store_name)
            product.add_stores(store)


if __name__ == "__main__":
    main()
