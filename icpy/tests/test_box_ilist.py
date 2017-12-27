# -*- coding: utf-8 -*-

from icpy.box import IntervalList

from interval import interval, inf


def test_instance1():
    x = IntervalList({'x': interval[0,1]})
    assert len(x) == 1
    assert x.width() == 1
    assert str(x) == "box{'x': interval([0.0, 1.0])}"
    assert not x.is_empty()
    assert x['x'] == interval[0,1]

    x['x'] = interval[10,20.5]
    assert len(x) == 1
    assert x.width() == 10.5
    assert str(x) == "box{'x': interval([10.0, 20.5])}"
    assert not x.is_empty()
    assert x['x'] == interval[10,20.5]

    x['y'] = interval[0,1]
    assert len(x) == 2
    assert x.width() == 10.5
    assert str(x) == "box{'x': interval([10.0, 20.5]), 'y': interval([0.0, 1.0])}"
    assert not x.is_empty()
    assert x['x'] == interval[10,20.5]
    assert x['y'] == interval[0,1]

    x['z'] = interval[0,inf]
    assert len(x) == 3
    assert x.width() == inf
    assert str(x) == "box{'x': interval([10.0, 20.5]), 'y': interval([0.0, 1.0]), 'z': interval([0.0, inf])}"
    assert not x.is_empty()
    assert x['x'] == interval[10,20.5]
    assert x['y'] == interval[0,1]
    assert x['z'] == interval[0,inf]


def test_instance2():
    x = IntervalList({'a': interval[0,1], 'b': interval[0,1]})
    assert len(x) == 2
    assert x.width() == 1
    assert str(x) == "box{'a': interval([0.0, 1.0]), 'b': interval([0.0, 1.0])}"
    assert not x.is_empty()
    assert x['a'] == interval[0,1]
    assert x['b'] == interval[0,1]


def test_instance3():
    x = IntervalList({'a': 0, 'b': 1}, [interval[0,1], interval[0,1]])
    assert len(x) == 2
    assert x.width() == 1
    assert str(x) == "box{'a': interval([0.0, 1.0]), 'b': interval([0.0, 1.0])}"
    assert not x.is_empty()
    assert x['a'] == interval[0,1]
    assert x['b'] == interval[0,1]


def test_empty():
    x = IntervalList({})
    assert len(x) == 0
    assert str(x) == 'box{}'
    assert x.is_empty()

