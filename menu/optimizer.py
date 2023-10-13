from itertools import groupby
from django.utils.translation import gettext_lazy as _

from menu.models import Element

# Constants
PK = Element._meta.pk.name
CHILD = Element.parent.field.related_query_name()


class Optimizer:
    """Keeps the existed menus schema.
    
    The application expects that the user to "walk" between menus and menu
    elements with a session. To optimize menu rendering, the `Optimizer`
    keeps information about existed element relations.
    """

    def __init__(self) -> None:
        self._queryset = Element.objects.values(PK, CHILD,)
        self.purge()

    def fetch(self) -> None:
        """Fetches the existed elements and creates relations.
        
        Creates "parent" and "childs" relations.
        """
        # Return if the data already fetched
        if self._fetched:
            return

        self._relations = list(self._queryset)

        # Keeps child -> parent
        self._parents: dict[int, int] = {
            _child: el.get(PK)
            for el in self._relations
            if (_child := el.get(CHILD))
        }

        # Keeps parent -> [childs]
        self._childs: dict[int, list[int]] = {
            parent_id: [
                _child for child in childs if (_child := child.get(CHILD))
            ] for parent_id, childs in groupby(
                self._relations, key=lambda el: el.get(PK),
            )
        }

        self._fetched = True

    def purge(self) -> None:
        """Clears all relation attributes."""
        self._relations: list = []
        self._parents: dict[int, int] = {}
        self._childs: dict[int, list[int]] = {}

        self._fetched = False

    def get_parent(self, child: int) -> int | None:
        """Returns parent by the given child."""
        return self._parents.get(child, None)

    def get_childs(self, parent: int) -> list[int]:
        """ Returns child list by the given parent.

        Raises:
            KeyError: if the given parent does not exist inside `_childs`.
        """
        try:
            return self._childs[parent]
        except KeyError:
            raise ValueError(
                _(
                    "Does not exist childs for the given parent element with "
                    f"{parent} pk."
                ),
            )

    def get_menu(self, element: int, menu: dict = {}):
        """Collects the given element childs and parent.
        
        Creates nested dictionary which contains all childs and all parents up
        to the root element and combines it.
        """
        if not self._fetched:
            self.fetch()

        childs = self.get_childs(element)
        parent = self.get_parent(element)

        _menu = {
            element: ({child: None for child in childs} | menu) or None
        }

        if parent:
            return self.get_menu(parent, _menu)

        return _menu

    @staticmethod
    def get_all_menu_items(
        menu,
        elements: list[int] | None = None,
    ) -> list[int]:
        """Returns all elements inside the given menu."""
        if elements is None:
            elements = []

        for element, childs in menu.items():
            elements.append(element)
            if childs is not None:
                Optimizer.get_all_menu_items(childs, elements)

        return elements
