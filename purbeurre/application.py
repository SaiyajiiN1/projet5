from settings import CATEGORIES
from purbeurre.models import Product, Category, Store, Favorite


class Application:
    """Represents the client application."""

    def __init__(self):
        """Initializes the new application."""
        self.next_menu = None

    def start(self):
        """Starts the application."""
        self.next_menu = self.home_menu

        while self.next_menu is not None:
            self.next_menu = self.next_menu()

    def get_user_choice(self, *options_collections):
        """Displays the menu and manages the user's response."""
        # We build an options dictionary
        counter = i = 0
        choices = {}
        for options in options_collections:
            if isinstance(options, list):
                for i, option in enumerate(options, start=counter + 1):
                    choices[str(i)] = option
                counter = i
            elif isinstance(options, dict):
                for key, option in options.items():
                    choices[str(key)] = option
            else:
                raise ValueError("options_collections must be lists or dicts")

        # The menu is displayed again as long as the user does not select a
        # valid choice.
        while True:
            # The menu options are displayed
            for key, choice in choices.items():
                print(f"{key}: {choice}")
            user_choice = input("\nQuel est votre choix ? ").strip()
            if user_choice in choices:
                return choices[user_choice]

    def home_menu(self):
        """Manages the home menu."""
        print("Welcome to the Pur Beurre application\n")
        choice = self.get_user_choice(
            ['Substitute a product', 'Consult the list of favorites'],
            {'q': "Exit the application"},
        )
        if choice == "Substitute a product":
            return self.categories_menu
        elif choice == "Consult the list of favorites":
            return self.favorite_list_menu
        else:
            return self.quit_menu

    def categories_menu(self):
        """Manages the categories menu."""
        print("\nChoose a category below\n")
        user_categories = Category.manager.get_by_names(*CATEGORIES)
        random_categories = Category.manager.get_with_excluded_names(
            *CATEGORIES, order_by=['RAND()'], limit=[10]
        )
        choice = self.get_user_choice(
            user_categories,
            random_categories,
            {'q': "Exit the application", 'h': "Return to home"},
        )

        if choice == "Exit the application":
            return self.quit_menu
        elif choice == "Return to home":
            return self.home_menu
        else:
            self.category = choice
            return self.category_products_menu

    def category_products_menu(self):
        """Manages the menu displaying the list of products in a category."""
        print("\nChoose a product below to substitute it\n")
        products = self.category.get_products(order_by=['RAND()'], limit=[20])
        choice = self.get_user_choice(
            products,
            {
                'q': "Exit the application",
                'b': "Return to the previous menu",
                'h': "Return to home",
            },
        )
        if choice == "Return to home":
            return self.home_menu
        elif choice == "Return to the previous menu":
            return self.categories_menu
        elif choice == "Exit the application":
            return self.quit_menu
        else:
            self.product = choice
            return self.substitutes_menu

    def substitutes_menu(self):
        """Manages the menu offering substitutes."""
        print("\nChoose a substitute suggested below\n")
        substitutes = Product.manager.find_substitutes_for_product(
            self.product, limit=[5]
        )
        choice = self.get_user_choice(
            substitutes,
            {
                'q': "Exit the application",
                'b': "Return to the previous menu",
                'h': "Return to home",
            },
        )
        if choice == "Return to home":
            return self.home_menu
        elif choice == "Return to the previous menu":
            return self.category_products_menu
        elif choice == "Exit the application":
            return self.quit_menu
        else:
            self.substitute = choice
            return self.substitute_detail_menu

    def substitute_detail_menu(self):
        """Manages the display of detailed information about the substitute."""
        print("\nHere is the substitute you have selected\n")
        print(self.substitute.format_info())
        print("\nDo you want to save this substitute as a favorite? ")
        choice = self.get_user_choice(['Yes', 'No'])
        if choice == "Yes":
            Favorite.manager.create(
                product=self.product, substitute=self.substitute
            )
            print(
                f"{self.substitute} was registered as a substitute "
                f"of {self.product}.\n"
            )
        return self.substitutes_menu

    def favorite_list_menu(self):
        """Manages the menu displaying the list of favorites."""
        favorites = Favorite.manager.get_all()
        if len(favorites) > 0:
            print("\nHere are the favorites you have saved\n")
        else:
            print("\nThere are no saved favorites\n")
        choice = self.get_user_choice(
            favorites,
            {
                'q': "Exit the application",
                'h': "Return to home",
            },
        )
        if choice == "Exit the application":
            return self.quit_menu
        elif choice == "Return to home":
            return self.home_menu
        else:
            self.selected_favorite = choice
            return self.favorite_details_menu

    def favorite_details_menu(self):
        """Manage the display of favorite details."""
        print("\nHere are the details of the selected favorite\n")
        print("The following original product:")
        print(self.selected_favorite.get_product().format_info())
        print("Can be substituted by:")
        print(self.selected_favorite.get_substitute().format_info())
        choice = self.get_user_choice(
            {
                'q': "Exit the application",
                'b': "Return to the previous menu",
                'h': "Return to home",
            }
        )
        if choice == "Exit the application":
            return self.quit_menu
        elif choice == "Return to the previous menu":
            return self.favorite_list_menu
        elif choice == "Return to home":
            return self.home_menu

    def quit_menu(self):
        """Manages the end menu of the application."""
        print("Goodbye !")
