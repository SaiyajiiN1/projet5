from purbeurre.models import Category


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
