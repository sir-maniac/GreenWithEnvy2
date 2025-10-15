# This file is part of gwe.
#
# Copyright (c) 2025 Ryan Bloomfield
#
# gwe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gwe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gwe.  If not, see <http://www.gnu.org/licenses/>.
#
# Based on deprecated library 'Dazzle', dzl-graph-column copyrighted by
#    Christian Hergert
#
import sys
import typing
from collections import deque
from typing import Any, Generic, TypeVar

# silence type error with deque
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

if typing.TYPE_CHECKING:
    from _typeshed import SupportsRichComparison
else:
    SupportsRichComparison: TypeAlias = Any


T = TypeVar('T', bound=SupportsRichComparison)
class GraphColumn(Generic[T]):
    name: str

    def __init__(self, name: str, max_len: int) -> None:
        self.name = name
        self._values: deque[T] = deque(maxlen=max_len)
        self._max_len: int = max_len

    @property
    def max_len(self) -> int:
        return self._max_len

    def append(self, value: T) -> None:
        self._values.append(value)

    def resize(self, new_max_len: int) -> None:
        new_values: deque[T] = deque(self._values, maxlen=new_max_len)
        self._max_len = new_max_len
        self._values = new_values

    def __len__(self) -> int:
        return len(self._values)

    def max_value(self) -> T:
        if len(self._values) == 0:
            raise RuntimeError("No samples in column")
        # dequeue can be iterated, but type checkers don't seem to think so
        return max(self._values)

    def min_value(self) -> T:
        if len(self._values) == 0:
            raise RuntimeError("No samples in column")
        # dequeue can be iterated, but type checkers don't seem to think so
        return min(self._values)


    def get_value(self, index: int) -> T:
        """
        Args:
            index (int): index into ring buffer

        Raises:
            IndexError: if index is out of range

        Returns:
            T: The value at `index`
        """
        return self._values[index]
    __getitem__ = get_value

    def set_value(self, index: int, value: T) -> None:
        """

        Args:
            index (int): the index into the ring buffer
            value (T): the value to set at `index`

        Raises:
            IndexError: if `index` is out of range
        """
        self._values[index] = value
    __setitem__ = set_value




