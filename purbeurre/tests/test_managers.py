
from purbeurre.models import Category, Product, ProductCategory


def test_basemanager_get_all_works_correctly():
    Category.manager.create(name="pizzas")
    Category.manager.create(name="pâtes à tartiner")

    categories = Category.manager.get_all()
    Category.manager.delete_all()

    categories.sort(key=lambda obj: obj.id)

    assert categories[0].name == "pizzas"
    assert categories[1].name == "pâtes à tartiner"
    assert isinstance(categories[0], Category)


def test_basemanager_get_by_id_works_correctly():
    pizzas = Category.manager.create(name="pizzas")
    pates_a_tartiner = Category.manager.create(name="pâtes à tartiner")

    pizzas_category = Category.manager.get_by_id(id=pizzas.id)
    Category.manager.delete_all()

    assert pizzas.id == pizzas_category.id


def test_productcategorymanager_adds_categories_correctly():
    nutella = Product.manager.create(
        id=1,
        name="Nutella",
        url="http",
        nutriscore="E",
        description="Info sur le produit",
    )
    pates_a_tartiner = Category.manager.create(name="Pâte à tartiner")
    produit_au_chocolat = Category.manager.create(name="Produits au chocolat")

    ProductCategory.manager.add_categories_to_product(
        nutella, pates_a_tartiner, produit_au_chocolat
    )

    associations = ProductCategory.manager.get_all()

    ProductCategory.manager.delete_all()
    Product.manager.delete_all()
    Category.manager.delete_all()

    assert len(associations) == 2


def test_productcategorymanager_adds_products_correctly():
    pizza_margherita = Product.manager.create(
        id=2,
        name="Pizza Margherita",
        url="http",
        nutriscore="E",
        description="Info sur le produit",
    )
    pizza_4_fromages = Product.manager.create(
        id=3,
        name="Pizza 4 fromages",
        url="http",
        nutriscore="E",
        description="Info sur le produit",
    )
    pizza = Category.manager.create(name="Pizza")

    ProductCategory.manager.add_products_to_category(
        pizza, pizza_margherita, pizza_4_fromages
    )

    associations = ProductCategory.manager.get_all()

    ProductCategory.manager.delete_all()
    Product.manager.delete_all()
    Category.manager.delete_all()

    assert len(associations) == 2


def test_productmanager_gets_products_by_category_correctly():
    pizza_margherita = Product.manager.create(
        id=2,
        name="Pizza Margherita",
        url="http",
        nutriscore="E",
        description="Info sur le produit",
    )
    pizza_4_fromages = Product.manager.create(
        id=3,
        name="Pizza 4 fromages",
        url="http",
        nutriscore="E",
        description="Info sur le produit",
    )
    pizza = Category.manager.create(name="Pizza")

    ProductCategory.manager.add_products_to_category(
        pizza, pizza_margherita, pizza_4_fromages
    )

    products = Product.manager.get_products_by_category(pizza)

    ProductCategory.manager.delete_all()
    Product.manager.delete_all()
    Category.manager.delete_all()

    assert len(products) == 2


def test_categorymanager_gets_categories_by_product_correctly():
    nutella = Product.manager.create(
        id=1,
        name="Nutella",
        url="http",
        nutriscore="E",
        description="Info sur le produit",
    )
    pates_a_tartiner = Category.manager.create(name="Pâte à tartiner")
    produit_au_chocolat = Category.manager.create(name="Produits au chocolat")

    ProductCategory.manager.add_categories_to_product(
        nutella, pates_a_tartiner, produit_au_chocolat
    )

    categories = Category.manager.get_categories_by_product(nutella)

    ProductCategory.manager.delete_all()
    Product.manager.delete_all()
    Category.manager.delete_all()

    assert len(categories) == 2
