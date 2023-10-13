from django import forms

from menu.models import Menu, Element


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ("name",)

    def handle_related_element(self, element: Element) -> None:
        """Updates related element name based on the current instance."""
        element.name = Element.get_root_name(self.instance.name)
        element.save()

    def _post_clean(self) -> None:
        """Handle related element changes on the form save."""
        related_element = (
            self.instance.get_root_element()
            if self.instance.name
            else Element()
        )

        super()._post_clean()

        self.handle_related_element(related_element)
