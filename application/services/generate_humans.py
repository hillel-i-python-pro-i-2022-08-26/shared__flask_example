import random
from collections.abc import Iterator

from app import faker
from application.models import Human
from application.typing import T_HUMAN


def generate_human() -> T_HUMAN:
    return Human(name=faker.first_name(), age=random.randint(10, 100))


def generate_humans(amount: int = 10) -> Iterator[T_HUMAN]:
    for _ in range(amount):
        yield generate_human()
