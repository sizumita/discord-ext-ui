from typing import Any


class ValueAble:
    def __init__(self, default: Any = None):
        self.value = default

    def __bool__(self) -> bool:
        return self.value.__bool__()

    def __bytes__(self) -> bytes:
        return self.value.__bytes__()

    def __complex__(self) -> complex:
        return self.value.__complex__()

    def __float__(self) -> float:
        return self.value.__float__()

    def __format__(self, format_spec: Any) -> str:
        return self.value.__format__(format_spec)

    def __int__(self) -> int:
        return self.value.__int__()

    def __repr__(self) -> str:
        return self.value.__repr__()

    def __str__(self) -> str:
        return self.value.__str__()

    def __eq__(self, other: Any) -> bool:
        return self.value.__eq__(other)

    def __ne__(self, other: Any) -> bool:
        return self.value.__ne__(other)

    def __hash__(self) -> Any:
        return self.value.__hash__()

    def __lt__(self, other: Any) -> bool:
        return self.value.__lt__(other)

    def __le__(self, other: Any) -> bool:
        return self.value.__le__(other)

    def __gt__(self, other: Any) -> bool:
        return self.value.__gt__(other)

    def __ge__(self, other: Any) -> bool:
        return self.value.__ge__(other)

    def __call__(self, *args: list, **kwargs: dict) -> Any:
        return self.value.__call__(*args, **kwargs)

    def __neg__(self) -> Any:
        return self.value.__neg__()

    def __sub__(self, other: Any) -> Any:
        return self.value.__sub__(other)

    def __pos__(self) -> Any:
        return self.value.__pos__()

    def __add__(self, other: Any) -> Any:
        return self.value.__add__(other)

    def __mul__(self, other: Any) -> Any:
        return self.value.__mul__(other)

    def __truediv__(self, other: Any) -> Any:
        return self.value.__truediv__(other)

    def __floordiv__(self, other: Any) -> Any:
        return self.value.__floordiv__(other)

    def __mod__(self, other: Any) -> Any:
        return self.value.__mod__(other)

    def __divmod__(self, other: Any) -> Any:
        return self.value.__divmod__(other)

    def __pow__(self, power: Any, modulo: Any = None) -> Any:
        return self.value.__pow__(power, modulo)

    def __lshift__(self, other: Any) -> Any:
        return self.value.__lshift__(other)

    def __rshift__(self, other: Any) -> Any:
        return self.value.__rshift__(other)

    def __and__(self, other: Any) -> Any:
        return self.value.__and__(other)

    def __xor__(self, other: Any) -> Any:
        return self.value.__xor__(other)

    def __or__(self, other: Any) -> Any:
        return self.value.__or__(other)

    def __abs__(self) -> Any:
        return self.value.__abs__()
