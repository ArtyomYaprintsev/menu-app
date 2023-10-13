from django.db import models
from django.db.models.query import QuerySet


class MenuManager(models.Manager):
    """Menu manager with additional `all_with_root` method.
    
    The menu and the root element are not obviously related. Manager provides
    additional method to fetch related elements.
    """

    def all_with_root(self, element_postfix: str) -> QuerySet:
        """Fetch all menus with related elements.

        Warning:
            Method supports only `sqlite3` database engine.
        """
        return self.get_queryset().extra(
            tables=["menu_element"],
            where=[f'menu_element.name like menu_menu.name || "{element_postfix}"'],
            select={"root": "menu_element.name", "root_id": "menu_element.id"},
        )
