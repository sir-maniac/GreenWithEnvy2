import pytest
from collections import deque
from gwe.model.graph_column import GraphColumn

def test_graph_column_init() -> None:
    col = GraphColumn[int]("Test", 5)
    assert col.name == "Test"
    assert col.max_len == 5
    assert isinstance(col._values, deque)
    assert col._values.maxlen == 5

def test_graph_column_append_and_get_value() -> None:
    col = GraphColumn[int]("Numbers", 3)
    col.append(1)
    col.append(2)
    col.append(3)
    assert col.get_value(0) == 1
    assert col.get_value(1) == 2
    assert col.get_value(2) == 3

def test_graph_column_ring_buffer_behavior() -> None:
    col = GraphColumn[int]("Numbers", 2)
    col.append(10)
    col.append(20)
    col.append(30)
    assert len(col._values) == 2
    assert list(col._values) == [20, 30]

def test_graph_column_index_error_on_get() -> None:
    col = GraphColumn[int]("Numbers", 2)
    col.append(5)
    with pytest.raises(IndexError):
        col.get_value(1)

def test_graph_column_set_value() -> None:
    col = GraphColumn[int]("Numbers", 2)
    col.append(100)
    col.append(200)
    col.set_value(0, 300)
    assert col.get_value(0) == 300

def test_graph_column_index_error_on_set() -> None:
    col = GraphColumn[int]("Numbers", 2)
    col.append(5)
    with pytest.raises(IndexError):
        col.set_value(1, 10)

def test_graph_column_getitem_setitem_aliases() -> None:
    col = GraphColumn[int]("Numbers", 2)
    col.append(1)
    col.append(2)
    assert col[0] == 1

    col[0] = 99
    assert col[0] == 99

def test_graph_column_overflow_and_indexing() -> None:
    col = GraphColumn[int]("Overflow", 3)
    col.append(1)
    col.append(2)
    col.append(3)
    col.append(4)
    col.append(5)
    # After 5 appends, only last 3 should remain: [3, 4, 5]
    assert len(col._values) == 3
    assert list(col._values) == [3, 4, 5]
    assert col.get_value(0) == 3
    assert col.get_value(1) == 4
    assert col.get_value(2) == 5

def test_graph_column_resize_smaller() -> None:
    col = GraphColumn[int]("Resize", 5)
    col.append(1)
    col.append(2)
    col.append(3)
    col.append(4)
    col.append(5)

    col.resize(3)
    # Only last 3 values should remain: [3, 4, 5]
    assert len(col._values) == 3
    assert list(col._values) == [3, 4, 5]
    assert col.get_value(0) == 3
    assert col.get_value(1) == 4
    assert col.get_value(2) == 5


#
#  max_value()
#

def test_graph_column_max_value_basic() -> None:
    col = GraphColumn[int]("Numbers", 5)
    col.append(10)
    col.append(20)
    col.append(5)
    col.append(15)
    assert col.max_value() == 20

def test_graph_column_max_value_negative_numbers() -> None:
    col = GraphColumn[int]("Negatives", 3)
    col.append(-10)
    col.append(-5)
    col.append(-20)
    assert col.max_value() == -5

def test_graph_column_max_value_floats() -> None:
    col = GraphColumn[float]("Floats", 4)
    col.append(1.1)
    col.append(2.2)
    col.append(0.5)
    assert col.max_value() == 2.2

def test_graph_column_max_value_raises_on_empty() -> None:
    col = GraphColumn[int]("Empty", 2)
    with pytest.raises(expected_exception=RuntimeError):
        col.max_value()

#
# min_value()
#

def test_graph_column_min_value_basic() -> None:
    col = GraphColumn[int]("Numbers", 5)
    col.append(10)
    col.append(20)
    col.append(5)
    col.append(15)
    assert col.min_value() == 5

def test_graph_column_min_value_negative_numbers() -> None:
    col = GraphColumn[int]("Negatives", 3)
    col.append(-10)
    col.append(-5)
    col.append(-20)
    assert col.min_value() == -20

def test_graph_column_min_value_floats() -> None:
    col = GraphColumn[float]("Floats", 4)
    col.append(1.1)
    col.append(2.2)
    col.append(0.5)
    assert col.min_value() == 0.5

def test_graph_column_min_value_raises_on_empty() -> None:
    col = GraphColumn[int]("Empty", 2)
    with pytest.raises(RuntimeError):
        col.min_value()