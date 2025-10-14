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
# Based on deprecated library 'Dazzle', dzl-graph-model copyrighted by
#    Christian Hergert
#

from math import e
from typing import Iterable, List, Optional

from gi.repository import GLib, GObject
from gi.repository.GObject import SignalFlags
from pytest import param

from .graph_column import GraphColumn

USEC_PER_SEC: int = 1000000

class GraphModelIter():
    """An iterator for each row in the model.
        Sets or gets values from each column.

        Start out in an invalid state, call next() to advance to the first row.
        Empty rows will return false on first call to next().
    """
    timestamp: property
    index: property

    def __init__(self, table: "Optional[GraphModel]", index: int) -> None:
        self._table: "Optional[GraphModel]" = table
        self._index: int = index
        self._timestamp: int = 0
        self._is_valid: bool = False

    def get_index(self) -> int:
        return self._index
    index = property(fget=get_index)

    def get_timestamp(self) -> int:
        if not self._is_valid:
            raise RuntimeError("Iterator is invalid")
        return self._timestamp
    timestamp = property(fget=get_timestamp)

    def next(self) -> bool:
        if self._table is None:
            return False

        self._index = self._index + 1
        if self._index < 0 or self._index >= len(self._table._timestamps):
            self._table = None # remove reference early
            self._is_valid = False
            return False

        self._timestamp = self._table._timestamps.get_value(self._index)
        self._is_valid = True
        return True

    def get_value(self, column: int) -> float:
        """_summary_

        Args:
            column (int): _description_

        Raises:
            ValueError: if `column` is out of range
            RuntimeError: if there are no samples

        Returns:
            float: The value at `column` in the current row
        """
        if not self._is_valid or self._table is None:
            raise RuntimeError("Iterator is invalid")

        if column >= len(self._table._columns) or column < 0:
            raise ValueError("Invalid Argument: column out of range")

        col = self._table._columns[column]
        if len(col) == 0:
            raise RuntimeError("No samples in model")
        return col.get_value(self._index)

    def set_value(self, column: int, value: float) -> None:
        """Sets an individual value within a specific column

        Args:
            column (int): the column to set
            value (float):  the new value of the column
        Raises:
            ValueError: if `column` is out of range
            RuntimeError: if there are no samples
        """
        if not self._is_valid or self._table is None:
            raise RuntimeError("Iterator is invalid")
        if column >= len(self._table._columns) or column < 0:
            raise ValueError("Invalid Argument: column out of range")

        col = self._table._columns[column]
        if len(col) == 0:
            raise RuntimeError("No samples in model")

        self._table._check_min_max(value)
        col.set_value(self._index, value )
        self._table.emit("changed")


class GraphModel(GObject.GObject):
    """Model to hold time series data for graphing.

    Signals:
        changed: Emitted when the model changes, such as when new samples are added.

    Properties:
        max_samples (int): The maximum number of samples to hold in the model. Default is 60.
        value_min (float): The minimum value for the graph's Y-axis. Default is 0.0.
        value_max (float): The maximum value for the graph's Y-axis. Default is 100.0.
        timespan (int): The time span in microseconds that the graph covers. Default is 60 seconds.

    """

    def __init__(self,
                 column_names: Iterable[str],
                 max_samples: int,
                 timespan: int = USEC_PER_SEC * 60,
                 value_min: float = 0.0,
                 value_max: float = 100.0) -> None:
        super().__init__()

        self._timestamps: GraphColumn[int] = GraphColumn('', max_samples)

        self._columns: List[GraphColumn[float]] = []
        for n in column_names:
            self._columns.append(GraphColumn(n, max_samples))

        self._max_samples: int = max_samples
        self._value_min: float = value_min
        self._value_max: float = value_max
        self._timespan: int = timespan

    def __len__(self) -> int:
        """Returns the number of samples in the model."""
        return len(self._timestamps)

    @GObject.Signal(flags=SignalFlags.RUN_LAST)
    def changed(self) -> None:
        """Emitted when the model changes, such as when new samples are added."""
        pass

    @GObject.Property(type=int, default=60)
    def max_samples(self) -> int:
        return self._max_samples

    @GObject.Property(type=float, default=0.0)
    def value_min(self) -> float:
        return self._value_min

    @value_min.setter
    def set_value_min(self, val: float) -> None:
        if val >= self._value_max:
            raise ValueError("Invalid Argument: value_min must be less than value_max")
        self._value_min = val
        self.notify("value_min")

    @GObject.Property(type=float, default=100.0)
    def value_max(self) -> float:
        return self._value_max

    @value_max.setter
    def set_value_max(self, val: float) -> None:
        if val <= self._value_min:
            raise ValueError("Invalid Argument: value_max must be greater than value_min")
        self._value_max = val
        self.notify("value_max")

    @GObject.Property(type=int, default=60 * USEC_PER_SEC)
    def timespan(self) -> int:
        """timespan in microseconds"""
        return self._timespan

    def get_iter_first(self) -> GraphModelIter:
        """
        Returns:
            GraphModelIter: The iterator
        """
        return GraphModelIter(self, -1)

    def append(self, timestamp: int, *values: float) -> None:
        if len(values) != len(self._columns):
            raise ValueError("Invalid Argument: values length does not match number of columns")

        self._timestamps.append(timestamp)
        for i, col in enumerate(self._columns):
            self._check_min_max(values[i])
            col.append(values[i])
        self.emit("changed")

    def get_column_max(self, column: int) -> float:
        if len(self._timestamps) == 0:
            raise RuntimeError("No samples in model")
        if column >= len(self._columns) or column < 0:
            raise ValueError("Invalid Argument: column out of range")
        col = self._columns[column]
        return col.max_value()

    def get_column_min(self, column: int) -> float:
        if len(self._timestamps) == 0:
            raise RuntimeError("No samples in model")
        if column >= len(self._columns) or column < 0:
            raise ValueError("Invalid Argument: column out of range")
        col = self._columns[column]
        return col.min_value()


    def get_iter_last(self) -> GraphModelIter:
        """

        Returns:
            GraphModelIter: the iterator
        """
        if len(self._timestamps) == 0:
            return GraphModelIter(None, -1)
        else:
            return GraphModelIter(self, len(self._timestamps) - 2)

    def get_end_time(self) -> int:
        if len(self._timestamps) != 0:
            # Safe to access [-1] since we checked length above
            return self._timestamps[-1]
        else:
            return GLib.get_monotonic_time()

    def _check_min_max(self, val) -> None:
        """update max and min values if `val` is outside of it"""
        if val > self._value_max:
            self.value_max = val
        elif val < self._value_min:
            self.value_min = val






