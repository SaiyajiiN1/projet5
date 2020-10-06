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
