from typing import Callable, TypeVar

T = TypeVar("T")


def some(predicate: Callable[[T], bool], targets: list[T]) -> T | None:
    return next(filter(predicate, targets), None)


def find_first(predicate: Callable[[T], bool], targets: list[T]) -> T:
    found = some(predicate, targets)
    if found is None:
        raise Exception("TargetNotFound")
    return found


def equals(a: str, b: str) -> bool:
    return a.lower() == b.lower()


def unique(values: list[str]) -> list[str]:
    return list(set(values))


def lower(values: list[str]) -> list[str]:
    return list(map(lambda v: v.lower(), values))
