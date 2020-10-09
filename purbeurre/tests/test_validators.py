from purbeurre.validators import ProductValidator

from purbeurre.tests import test_data as data


def test_valid_products_are_kept_by_product_validator():
    valid_products = data.get_valid_products()
    validator = ProductValidator()
    filtered_products = validator.filter(valid_products)
    assert len(filtered_products) == len(valid_products)


def test_invalid_products_are_removed_by_product_validator():
    invalid_products = data.get_invalid_products()
    validator = ProductValidator()
    filtered_products = validator.filter(invalid_products)
    assert len(filtered_products) == 0


def test_only_invalid_products_are_removed_by_product_validator():
    invalid_products_but_one = data.get_invalid_with_one_valid_product()
    validator = ProductValidator()
    filtered_products = validator.filter(invalid_products_but_one)
    assert len(filtered_products) == 1
