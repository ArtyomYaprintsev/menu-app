import string
from typing import Any
from random import choices
from django.core.management.base import BaseCommand

from menu.models import Menu, Element
from menu.forms import MenuForm


class Command(BaseCommand):
    help = """
    Creates two menus with random name and related elements. Total
    element deep: 2, menu related elements count: 6 (exclude root element).
    """

    def _get_random_postfix(self, length: int=8) -> str:
        return ''.join(
            choices(
                string.ascii_uppercase + string.digits,
                k=length,
            )
        )

    def create_menu(self, basename: str) -> Menu:
        basename = f"{basename}-{self._get_random_postfix()}"

        form = MenuForm(data={"name": basename})
        form.is_valid()

        return form.save()

    def create_childs(self, parent: Element, count: int=3) -> list[Element]:
        return Element.objects.bulk_create(
            Element(parent=parent, name=f"{parent.get_name()}-child-{index}")
            for index in range(count)
        )

    def fill_menu(self, menu: Menu) -> None:
        root = menu.get_root_element()

        elements = self.create_childs(root)

        self.create_childs(elements[0], 2)
        self.create_childs(elements[1], 1)

    def produce_menu(self, name: str="demo") -> None:
        menu = self.create_menu(name)
        self.fill_menu(menu)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created "%s" menu' % menu.name)
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        for _ in range(2):
            self.produce_menu()
