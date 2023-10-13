import string
from typing import Any
from random import choices
from django.core.management.base import BaseCommand

from menu.models import Menu, Element
from menu.forms import MenuForm


class Command(BaseCommand):
    """Provides functionality to create data for demo.

    Creates menu and related elements to make the demonstration easier.
    """

    help = """
    Creates two menus with random name and related elements. Total
    element deep: 2, menu related elements count: 6 (exclude root element).
    """

    def _get_random_postfix(self, length: int=8) -> str:
        """Returns random string with the given length."""
        return ''.join(
            choices(
                string.ascii_uppercase + string.digits,
                k=length,
            )
        )

    def create_menu(self, basename: str) -> Menu:
        """Creates `Menu` instance with the given basename.
        
        Appends to the given `basename` random postfix.
        """
        basename = f"{basename}-{self._get_random_postfix()}"

        form = MenuForm(data={"name": basename})
        form.is_valid()

        return form.save()

    def create_childs(self, parent: Element, count: int=3) -> list[Element]:
        """Creates child `Element` instances related to the given parent."""
        return Element.objects.bulk_create(
            Element(parent=parent, name=f"{parent.get_name()}-child-{index}")
            for index in range(count)
        )

    def fill_menu(self, menu: Menu) -> None:
        """Fills the given `Menu` instance with an elements."""
        root = menu.get_root_element()

        elements = self.create_childs(root)

        self.create_childs(elements[0], 2)
        self.create_childs(elements[1], 1)

    def produce_menu(self, name: str="demo") -> None:
        """Creates and fills menu based on the given name."""
        menu = self.create_menu(name)
        self.fill_menu(menu)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created "%s" menu' % menu.name)
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        for _ in range(2):
            self.produce_menu()
