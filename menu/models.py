from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from menu.managers import MenuManager


class Menu(models.Model):
    name = models.CharField(_("name"), max_length=128, unique=True)

    objects = MenuManager()

    class Meta:
        verbose_name = _("menu")
        verbose_name_plural = _("menus")
        ordering = ["name",]

    def __str__(self) -> str:
        return self.name

    def get_root_element(self) -> "Element":
        return Element.objects.get(
            name__regex=Element.get_root_name(self.name),
        )


class Element(models.Model):
    ROOT_POSTFIX = "-root"

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        verbose_name=_("parent"),
        related_name="children",
        blank=True, null=True,
    )

    name = models.CharField(_("name"), max_length=128)

    class Meta:
        verbose_name = _("element")
        verbose_name_plural = _("elements")
        ordering = ["name"]
        unique_together = ["parent", "name"]

    def clean(self) -> None:
        if self.parent is None or self.name.endswith(self.ROOT_POSTFIX):
            if not (
                self.parent is None
                and self.name.endswith(self.ROOT_POSTFIX)
            ):
                raise ValidationError(
                    _(
                        "Name of the element with None parent must ends with "
                        "%(postfix)s, but %(name)s was given."
                    ),
                    params={
                        "postfix": self.ROOT_POSTFIX,
                        "name": self.name,
                    },
                )

        return super().clean()

    def __str__(self) -> str:
        return f"{self.parent.name if self.parent else 'null'}/{self.name}"

    @classmethod
    def get_root_name(cls, name: str) -> str:
        return f"{name}{cls.ROOT_POSTFIX}"

    @property
    def is_root(self) -> bool:
        return not self.parent

    def get_name(self) -> str:
        if not self.is_root:
            return self.name

        return "-".join(self.name.split("-")[:-1])
