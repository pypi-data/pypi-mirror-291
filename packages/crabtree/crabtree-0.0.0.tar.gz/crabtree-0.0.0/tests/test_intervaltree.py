from crabtree import Interval, IntervalTree
import pytest


@pytest.fixture
def interval_tree():
    tree = IntervalTree([
        Interval(2, 3),
        Interval(4, 7),
        Interval(6, 9),
        Interval(12, 15),
    ])
    tree.display()
    return tree


def test_overlap(interval_tree: IntervalTree):
    intersection = set(interval_tree.overlap(Interval(5, 14)))
    assert intersection == {Interval(4, 7), Interval(6, 9), Interval(12, 15)}

    
def test_add(interval_tree: IntervalTree):
    interval_tree.add(Interval(8, 14))