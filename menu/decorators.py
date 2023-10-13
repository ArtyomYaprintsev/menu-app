from functools import wraps
from typing import Callable

from menu import OPTIMIZER
from menu.optimizer import Optimizer


def provide_optimizer(func: Callable):
    """Provides decorator which allows to interact with `Optimizer`."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Provides `Optimizer` kwarg to the decorated function.
        
        Initializes `OPTIMIZER` 'menu' app variable if it is `None`.
        """
        global OPTIMIZER

        if OPTIMIZER is None:
            OPTIMIZER = Optimizer()

        return func(*args, optimizer=OPTIMIZER, **kwargs)

    return wrapper
