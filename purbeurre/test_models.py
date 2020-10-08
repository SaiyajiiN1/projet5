from purbeurre import models


def test_product_model_can_be_instantiated():
    product = models.Product(
        name="Pizza",
        nutriscore="D",
        url="http://www.openclassrooms.com",
        description="Plus d'infos sur ce produit"
    )
    assert product.name == "Pizza"
    assert product.nutriscore == "D"
    assert product.url == "http://www.openclassrooms.com"
    assert product.description == "Plus d'infos sur ce produit"
    assert product.id is None


def test_category_model_can_be_instantiated():
    category = models.Category(name="Pizzas")
    assert category.name == "Pizzas"
    assert category.id is None


def test_store_model_can_be_instantiated():
    store = models.Store(name="Carrefour")
    assert store.id is None
    assert store.name == "Carrefour"
