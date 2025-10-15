import pytest
from gwe.model.graph_model import GraphModel, GraphModelIter, USEC_PER_SEC
from gwe.model.graph_column import GraphColumn
from gi.repository import GLib

class DummyValue:
    def __init__(self, value):
        self.value = value

def test_graph_model_initialization():
    model = GraphModel(['col1', 'col2'], max_samples=5)
    assert model.max_samples == 5
    assert model.value_min == 0.0
    assert model.value_max == 100.0
    assert model.timespan == USEC_PER_SEC * 60

def test_graph_model_iter_set_get_value():
    model = GraphModel(['col1'], max_samples=3)
    # Set up timestamps and values
    for i in range(3):
        model._timestamps.append(i + 1)
        model._columns[0].append(i * 10)
    iter = model.get_iter_first()
    assert iter.next() is True
    assert iter.get_value(0) == 0
    assert iter.next() is True
    assert iter.get_value(0) == 10
    assert iter.next() is True
    assert iter.get_value(0) == 20
    assert iter.next() is False

def test_graph_model_iter_set_value():
    model = GraphModel(['col1'], max_samples=2)
    model._timestamps.append(1)
    model._columns[0].append(1)
    iter = model.get_iter_first()
    assert iter.next() is True
    iter.set_value(0, 42)
    assert iter.get_value(0) == 42
    assert iter.next() is False

def test_graph_model_iter_next_returns_false_when_table_none():
    model = GraphModel(['col1'], max_samples=1)
    iter = model.get_iter_first()
    iter._table = None
    assert iter.next() is False

def test_graph_model_iter_empty():
    model = GraphModel(['col1'], max_samples=1)
    iter = model.get_iter_first()

    # first call to next() returns false
    assert iter.next() is False

    # raises RuntimeError when iter is invalid

    with pytest.raises(RuntimeError):
        iter.set_value(0, 10)

    with pytest.raises(RuntimeError):
        iter.get_value(0)

    iter = model.get_iter_last()
    # first call to next() returns false
    assert iter.next() is False

    # raises RuntimeError when iter is invalid

    with pytest.raises(RuntimeError):
        iter.set_value(0, 10)

    with pytest.raises(RuntimeError):
        iter.get_value(0)


def test_graph_model_iter_next_returns_false_at_last_index():
    model = GraphModel(['col1'], max_samples=2)
    model._columns[0].append(1)
    model._timestamps.append(1)
    model._columns[0].append(2)
    model._timestamps.append(2)
    iter = model.get_iter_last()
    assert iter.next() is True
    assert iter.next() is False

def test_graph_model_iter_index_and_timestamp_properties():
    model = GraphModel(['col1'], max_samples=1)
    model._columns[0].append(1)
    model._timestamps.append(123)
    iter = model.get_iter_first()
    assert iter.index == -1
    assert iter.next() is True
    assert iter.index == 0
    assert iter.timestamp == 123

def test_graph_model_get_end_time_returns_last_timestamp():
    model = GraphModel(['col1'], max_samples=1)
    model._timestamps.append(555)
    assert model.get_end_time() == 555

def test_graph_model_get_end_time_returns_monotonic_time_on_index_error(monkeypatch):
    model = GraphModel(['col1'], max_samples=1)
    monkeypatch.setattr(GLib, "get_monotonic_time", lambda: 999)
    assert model.get_end_time() == 999

def test_graph_model_iter_get_value_invalid_column():
    model = GraphModel(['col1'], max_samples=1)
    model._timestamps.append(1)
    iter = model.get_iter_first()
    assert iter.next() is True
    with pytest.raises(ValueError):
        iter.get_value(2)

def test_graph_model_iter_set_value_invalid_column():
    model = GraphModel(['col1'], max_samples=1)
    model._timestamps.append(1)
    iter = model.get_iter_first()
    assert iter.next() is True
    with pytest.raises(ValueError):
        iter.set_value(2, 123)

def test_graph_model_ring_buffer_limits():
    model = GraphModel(['col1'], max_samples=3)
    model._columns[0].append(1)
    model._timestamps.append(10)
    model._columns[0].append(2)
    model._timestamps.append(20)
    model._columns[0].append(3)
    model._timestamps.append(30)
    iter = model.get_iter_first()
    assert iter.next() is True
    assert iter.get_value(0) == 1

    iter = model.get_iter_last()
    assert iter.next() is True
    assert iter.get_value(0) == 3
    assert iter.get_timestamp() == 30
    assert iter.next() is False

    model._columns[0].append(4)
    model._timestamps.append(40)
    model._columns[0].append(5)
    model._timestamps.append(50)

    iter = model.get_iter_first()
    assert iter.next() is True
    assert iter.get_value(0) == 3
    assert iter.get_timestamp() == 30

    iter = model.get_iter_last()
    assert iter.next() is True
    assert iter.get_value(0) == 5
    assert iter.get_timestamp() == 50

def test_graph_model_iter_runtime_exceptions():
    # 1. Invalid iterator (no table)
    iter_invalid = GraphModelIter(None, -1)
    with pytest.raises(RuntimeError):
        iter_invalid.get_value(0)

    # 2. Invalid iterator (not advanced)
    model = GraphModel(['col1'], max_samples=1)
    iter_empty = GraphModelIter(model, -1)
    with pytest.raises(RuntimeError):
        iter_empty.get_value(0)

    # 3. Invalid column index
    model._timestamps.append(123)
    model._columns[0].append(42)
    iter_valid = GraphModelIter(model, -1)
    iter_valid.next()
    with pytest.raises(ValueError):
        iter_valid.get_value(100)

    # 4. No samples in column
    model2 = GraphModel(['col1'], max_samples=1)
    model2._timestamps.append(123)
    iter_no_samples = GraphModelIter(model2, -1)
    iter_no_samples.next()
    with pytest.raises(RuntimeError):
        iter_no_samples.get_value(0)

    # 5. next() not called
    model2 = GraphModel(['col1'], max_samples=1)
    model2._timestamps.append(123)
    model2._columns[0].append(42)
    iter_no_next = model2.get_iter_first()
    with pytest.raises(RuntimeError):
        t = iter_no_next.timestamp
    with pytest.raises(RuntimeError):
        iter_no_next.get_value(0)
