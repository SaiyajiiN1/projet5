def remove_unuseful_fields(product):
    useful_fields = {
        'code', 'product_name', 'categories', 'stores', 'nutriscore_grade',
        'url', 'generic_name'
    }
    for field in product.keys() - useful_fields:
        del product[field]


def transform_fields_into_lowercase_letters(product):
    fields = {
        'product_name', 'categories', 'stores', 'nutriscore_grade',
        'generic_name'
    }
    for field in fields:
        product[field] = product[field].lower()


def transform_categories_into_list(product):
    product['categories'] = [
        category.strip() for category in product['categories'].split(',')
    ]


def transform_stores_into_list(product):
    product['stores'] = [
        category.strip() for category in product['stores'].split(',')
    ]


def transform_field_names(product):
    transformations = {
        "code": "id",
        "product_name": "name",
        "generic_name": "description",
        "nutriscore_grade": "nutriscore"
    }
    for old_field, new_field in transformations.items():
        product[new_field] = product[old_field]
        del product[old_field]


class ProductNormalizer:
    """Object used to normalize product dictionaries."""

    normalizers = [
        remove_unuseful_fields,
        transform_fields_into_lowercase_letters,
        transform_categories_into_list,
        transform_stores_into_list,
        transform_field_names
    ]

    def normalize(self, product):
        """Normalize each product in the product list
         provided.
        """
        for normalizer in self.normalizers:
            normalizer(product)

    def normalize_all(self, products):
        """Normalize each product in the product list
         provided.
        """
        for product in products:
            self.normalize(product)
