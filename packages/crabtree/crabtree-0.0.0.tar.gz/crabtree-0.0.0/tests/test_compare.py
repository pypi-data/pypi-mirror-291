import random
from typing import Literal, Sequence
import intervaltree
import crabtree
import pytest


n = 10000
CREATION_MODE: Literal["constructor", "add"] = "add"


@pytest.fixture(scope="module")
def intervals() -> list[tuple[int, int]]:
    i: list[tuple[int, int]] = []
    for _ in range(n):
        start = random.randint(0, n*n)
        end = start + random.randint(1, n)
        i.append((start, end))

    return i


@pytest.fixture(scope="module")
def interval_for_overlap() -> tuple[int, int]:
    start = random.randint(0, n*100)
    end = start + random.randint(0, n*50)
    return (start, end)


@pytest.fixture(scope="module")
def interval_for_remove(intervals: list[tuple[int, int]]) -> tuple[int, int]:
    return random.choice(intervals)


@pytest.fixture(scope="module")
def point_for_at() -> int:
    return random.randint(0, n)


@pytest.fixture(scope="class")
def intervaltree_tree(intervals):
    if CREATION_MODE == "constructor":
        return intervaltree.IntervalTree.from_tuples(intervals)

    intervaltree_tree = intervaltree.IntervalTree()
    for i in intervals:
        intervaltree_tree.addi(*i)
    return intervaltree_tree


@pytest.fixture(scope="class")
def crabtree_tree(intervals):
    if CREATION_MODE == "constructor":
        ct_intervals = [crabtree.Interval(s, e) for s, e in intervals]
        return crabtree.IntervalTree(ct_intervals)

    crabtree_tree = crabtree.IntervalTree([])
    for i in intervals:
        crabtree_tree.add(crabtree.Interval(*i))
    return crabtree_tree


def test_overlap(intervaltree_tree, crabtree_tree, interval_for_overlap):
    intervaltree_result = intervaltree_tree.overlap(*interval_for_overlap)
    crabtree_result = crabtree_tree.overlap(crabtree.Interval(*interval_for_overlap))
    assert_eq(crabtree_result, intervaltree_result)


def test_at(intervaltree_tree, crabtree_tree, point_for_at):
    intervaltree_result = intervaltree_tree.at(point_for_at)
    crabtree_result = crabtree_tree.at(point_for_at)
    assert_eq(crabtree_result, intervaltree_result)


def test_merge_overlaps(intervaltree_tree, crabtree_tree):
    intervaltree_tree.merge_overlaps(strict=False)
    crabtree_tree.merge_overlaps()
    assert_eq(crabtree_tree.intervals, intervaltree_tree.all_intervals)


def test_overlaps_interval(intervaltree_tree, crabtree_tree, interval_for_overlap):
    intervaltree_result = intervaltree_tree.overlaps(*interval_for_overlap)
    crabtree_result = crabtree_tree.overlaps_interval(crabtree.Interval(*interval_for_overlap))
    assert crabtree_result == intervaltree_result


def test_overlaps_point(intervaltree_tree, crabtree_tree, point_for_at):
    intervaltree_result = intervaltree_tree.overlaps(point_for_at)
    crabtree_result = crabtree_tree.overlaps_point(point_for_at)
    assert crabtree_result == intervaltree_result


def test_remove(intervaltree_tree, crabtree_tree, interval_for_remove):
    intervaltree_tree.removei(*interval_for_remove)
    crabtree_tree.remove(crabtree.Interval(*interval_for_remove))
    assert_eq(crabtree_tree.sorted_intervals(), sorted(intervaltree_tree.all_intervals))


def assert_eq(ct, it):
    assert set(ct) == set(intervaltree_to_crabtree(it))


def intervaltree_to_crabtree(i: tuple[int, int] | intervaltree.Interval | Sequence[intervaltree.Interval]) -> crabtree.Interval:
    if isinstance(i, tuple):
        return crabtree.Interval(*i)

    if isinstance(i, intervaltree.Interval):
        return crabtree.Interval(i.begin, i.end)

    return [crabtree.Interval(x.begin, x.end) for x in i]
