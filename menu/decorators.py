from functools import wraps
from typing import Callable

from menu import OPTIMIZER
from menu.optimizer import Optimizer


def provide_optimizer(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global OPTIMIZER

        if OPTIMIZER is None:
            OPTIMIZER = Optimizer()

        return func(*args, optimizer=OPTIMIZER, **kwargs)

    return wrapper
