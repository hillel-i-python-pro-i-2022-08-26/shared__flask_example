from collections.abc import Iterator
from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from application.models import Human

T_ITERATOR_WITH_INTEGERS: TypeAlias = Iterator[int]

T_HUMAN: TypeAlias = "Human"
