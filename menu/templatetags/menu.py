from django.template import Library
from django.utils.translation import gettext as _

from menu.models import Element
from menu.optimizer import Optimizer
from menu.decorators import provide_optimizer


register = Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag("element.html", takes_context=True)
def draw_element(context, element: int, name: str):
    query_current = context.get("query")
    menu = context.get("menu")

    query_to_element = "&".join(
        f'{_menu}={element if _menu == menu else current_element}'
        for _menu, current_element in query_current.items()
    )
    active_element: str = query_current.get(menu)

    return {
        "name": name,
        "query": "?" + query_to_element,
        "is_active": str(element) == active_element,
    }


@register.inclusion_tag("elements.html", takes_context=True)
def draw_element_list(context, elements,):
    return {
        "elements": elements,
        **{
            param: context.get(param)
            for param in ["menu", "query", "element_names"]
        },
    }


@register.inclusion_tag(
    "menu.html",
    name="draw_menu",
    takes_context=True,
)
@provide_optimizer
def draw_menu(context, menu: str, **kwargs):
    optimizer: Optimizer = kwargs.get("optimizer")

    active_element = context["request"].GET.get(menu)

    if not active_element.isdigit():
        raise ValueError(
            _("Menu parameter must be a number, check query parameters."),
        )

    active_menu = optimizer.get_menu(int(active_element))
    element_names = {
        element.id: element.name
        for element in Element.objects.filter(
            pk__in=Optimizer.get_all_menu_items(active_menu),
        )
    }

    return {
        "elements": active_menu,
        "element_names": element_names,

        "menu": menu,
        "query": context["request"].GET,
    }
