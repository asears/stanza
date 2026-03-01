from __future__ import annotations

from collections.abc import Callable
from typing import Any


def _readonly_setter(self: Any, name: str) -> None:
    full_classname = self.__class__.__module__
    if full_classname is None:
        full_classname = self.__class__.__qualname__
    else:
        full_classname += '.' + self.__class__.__qualname__
    raise ValueError(f'Property "{name}" of "{full_classname}" is read-only.')

class StanzaObject:
    """
    Base class for all Stanza data objects that allows for some flexibility handling annotations
    """

    @classmethod
    def add_property(cls, name: str, default: Any = None, getter: Callable[[Any], Any] | None = None, setter: Callable[[Any, Any], None] | None = None) -> None:
        """
        Add a property accessible through self.{name} with underlying variable self._{name}.
        Optionally setup a setter as well.
        """

        if hasattr(cls, name):
            raise ValueError(f'Property by the name of {name} already exists in {cls}. Maybe you want to find another name?')

        setattr(cls, f'_{name}', default)
        if getter is None:
            getter = lambda self: getattr(self, f'_{name}')
        if setter is None:
            setter = lambda self, value: _readonly_setter(self, name)

        setattr(cls, name, property(getter, setter))

