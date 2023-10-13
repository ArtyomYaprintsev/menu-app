from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from menu.models import Menu, Element
from menu.forms import MenuForm


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    form = MenuForm


class ChildsInline(admin.TabularInline):
    model = Element
    fields = ("name",)
    show_change_link = True

    verbose_name = _("child")
    verbose_name_plural = _("childs")

    extra = 0

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    inlines = [ChildsInline,]

    def get_readonly_fields(self, request: HttpRequest, obj: Element | None = ...):
        if obj and obj.is_root:
            return self.readonly_fields + ("name",)

        return self.readonly_fields
