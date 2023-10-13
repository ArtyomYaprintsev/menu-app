from django.db.models import signals
from django.dispatch import receiver

from menu.models import Menu, Element
from menu.decorators import provide_optimizer


@receiver(
    signal=signals.post_delete,
    sender=Menu,
    dispatch_uid="delete_root_cascade",
)
def delete_root_cascade(instance: Menu, **kwargs):
    """Deletes related root element after the `Menu` instance deletion."""
    try:
        instance.get_root_element().delete()
    except Element.DoesNotExist:
        pass


@receiver(
    signal=signals.post_save,
    sender=Element,
    dispatch_uid="purge_optimizer_on_element_save",
)
@receiver(
    signal=signals.post_delete,
    sender=Element,
    dispatch_uid="purge_optimizer_on_element_delete",
)
@provide_optimizer
def purge_optimizer_on_element_signal(**kwargs):
    """Purges `Optimizer` on each element save or delete signal.
    
    An element creation, update or deletion means that menu scheme changed, to
    handle it `Optimizer` will purge all fetched data to show real information.
    """
    optimizer = kwargs.get("optimizer")
    optimizer.purge()
