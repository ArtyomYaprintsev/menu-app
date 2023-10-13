from typing import NamedTuple
from django.urls import reverse
from django.shortcuts import render, redirect

from menu.models import Menu, Element


class MenuWithRoot(NamedTuple):
    id: int
    name: str
    root_id: int
    root: str


def show_menus(request):
    menus: list[MenuWithRoot] = [
        MenuWithRoot(menu.id, menu.name, menu.root_id, menu.root)
        for menu in Menu.objects.all_with_root(
            Element.ROOT_POSTFIX,
        )
    ]

    if not all(menu.name in request.GET for menu in menus):
        query_params = "&".join(
            f'{menu.name}={request.GET.get(menu.name, menu.root_id)}'
            for menu in menus
        )
        return redirect(reverse("menus") + "?" + query_params)

    return render(request, "menus.html", context={
        "menus": menus,
    })
