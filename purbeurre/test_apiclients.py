from purbeurre.apiclients import OpenfoodfactsClient


def test_get_products_by_popularity_downloads_the_right_number_of_products():
    client = OpenfoodfactsClient(lang="fr")
    products = client.get_products_by_popularity(
        page_size=20, number_of_pages=3
    )
    assert len(products) == 60
