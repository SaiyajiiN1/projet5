"""This module contains classes allowing easy access
to different APIS.
"""

import requests


class OpenfoodfactsClient:
    """Represents an interface to the Openfoodfacts API."""

    def __init__(self, lang="fr"):
        """Client builder openfoodfacts.

        Args:
            lang (str): specifies the API language we want
            to access. Support "en", "fr", "world", the default value
            is "fr".

        Raises:
            ValueError: if lang receives a value which is not supported.

        """
        if lang not in ("fr", "en", "world"):
            raise ValueError('lang supports values "fr", "en" and world"')
        self.url = f"https://{lang}.openfoodfacts.org/cgi/search.pl"

    def get_procuts_by_popularity(self, page_size=100, numbe_of_pages=1):
        """Downloads products from openfoodfacts REST API in order of popularity

        Args:
            page_size (int): number of products to download per page.
            The supported values are 20, 50, 100, 250, 500, 1000.
            Default value is 100.
            number_of_pages (int): number of pages to download.
            Default value is 1.

        Return:
            A list of dictionaries describing the products of openfoodfacts
            downloaded. If a network error occurs, the returned list
            is empty.

        Raises:
            ValueError if page_size is not a supported value.

        """
        if page_size not in (20, 50, 100, 250, 500, 1000):
            raise ValueError(
                "page_size must have a value of"
                "20, 50, 100, 250, 500, 1000"
            )
        products = []
        for page in range(1, number_of_pages+1):
            params = {
                "action": "process",
                "json": True,
                "sort_by": "unique_scans_n",  # popularity
                "page_size": page_size,
                "page": page
            }
            try:
                reponse = requests.get(self.url, params=params)
                response.raise_for_status()
            except requests.exceptions.Request:
                return []  # In the event of an error, an empty list is returned

            data = response.json().get("products")
            if data is not None:
                products.extend(data)

        return products
