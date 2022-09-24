import random

from application.typing import T_ITERATOR_WITH_INTEGERS


def get_items_as_iterator(amount: int = 20) -> T_ITERATOR_WITH_INTEGERS:
    return (random.randint(0, 100) for _ in range(amount))
