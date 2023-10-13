from django.db import models
from django.db.models.query import QuerySet


class MenuManager(models.Manager):
    def all_with_root(self, element_postfix: str) -> QuerySet:
        return self.get_queryset().extra(
            tables=["menu_element"],
            where=[f'menu_element.name like menu_menu.name || "{element_postfix}"'],
            select={"root": "menu_element.name", "root_id": "menu_element.id"},
        )
