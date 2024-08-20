import random
import intervaltree
import crabtree
import pytest


n = 10000


@pytest.fixture(scope="class")
def intervals() -> list[tuple[int, int]]:
    i: list[tuple[int, int]] = []
    for _ in range(n):
        start = random.randint(0, n*100)
        end = start + random.randint(1, n*50)
        i.append((start, end))

    return i


@pytest.fixture(scope="class")
def interval_for_overlap() -> tuple[int, int]:
    start = random.randint(0, n*100)
    end = start + random.randint(0, n*50)
    return (start, end)


@pytest.fixture(scope="class")
def point_for_at() -> int:
    return random.randint(0, n)


@pytest.fixture(scope="class")
def intervaltree_tree(intervals):
    return intervaltree.IntervalTree.from_tuples(intervals)


@pytest.fixture(scope="class")
def crabtree_tree(intervals):
    ct_intervals = [crabtree.Interval(s, e) for s, e in intervals]
    return crabtree.IntervalTree(ct_intervals)


@pytest.mark.benchmark(group="instanciation")
class TestInstanciation:
    def test_intervaltree(self, benchmark, intervals):
        benchmark(intervaltree.IntervalTree.from_tuples, intervals)

    def test_crabtree(self, benchmark, intervals):
        ct_intervals = [crabtree.Interval(s, e) for s, e in intervals]
        benchmark(crabtree.IntervalTree, ct_intervals)


@pytest.mark.benchmark(group="overlap")
class TestOverlap:
    def test_intervaltree(self, benchmark, intervaltree_tree, interval_for_overlap):
        benchmark(intervaltree_tree.overlap, *interval_for_overlap)

    def test_crabtree(self, benchmark, crabtree_tree, interval_for_overlap):
        ct_interval_for_overlap = crabtree.Interval(*interval_for_overlap)
        benchmark(crabtree_tree.overlap, ct_interval_for_overlap)


@pytest.mark.benchmark(group="at")
class TestAt:
    def test_intervaltree(self, benchmark, intervaltree_tree, point_for_at):
        benchmark(intervaltree_tree.at, point_for_at)

    def test_crabtree(self, benchmark, crabtree_tree, point_for_at):
        benchmark(crabtree_tree.at, point_for_at)


@pytest.mark.benchmark(group="add")
class TestAdd:
    def test_intervaltree(self, benchmark, intervaltree_tree, interval_for_overlap):
        benchmark(intervaltree_tree.addi, *interval_for_overlap)

    def test_crabtree(self, benchmark, crabtree_tree, interval_for_overlap):
        benchmark(crabtree_tree.add, crabtree.Interval(*interval_for_overlap))


@pytest.mark.benchmark(group="remove")
class TestRemove:
    def test_intervaltree(self, benchmark, intervaltree_tree, intervals):
        to_remove = random.choice(intervals)
        # benchmark(intervaltree_tree.removei, *to_remove)
        benchmark.pedantic(
            intervaltree_tree.removei,
            args=to_remove,
            setup=lambda: intervaltree_tree.addi(*to_remove),
        )

    def test_crabtree(self, benchmark, crabtree_tree, intervals):
        to_remove = random.choice(intervals)
        benchmark.pedantic(
            crabtree_tree.remove,
            args=(crabtree.Interval(*to_remove),),
            setup=lambda: crabtree_tree.add(crabtree.Interval(*to_remove),)
        )


@pytest.mark.benchmark(group="merge_overlaps")
class TestMergeOverlaps:
    def test_intervaltree(self, benchmark, intervaltree_tree):
        benchmark(intervaltree_tree.merge_overlaps)

    def test_crabtree(self, benchmark, crabtree_tree):
        benchmark(crabtree_tree.merge_overlaps)


@pytest.mark.benchmark(group="overlaps_interval")
class TestOverlapsInterval:
    def test_intervaltree(self, benchmark, intervaltree_tree, interval_for_overlap):
        benchmark(intervaltree_tree.overlaps, *interval_for_overlap)

    def test_crabtree(self, benchmark, crabtree_tree, interval_for_overlap):
        ct_interval_for_overlap = crabtree.Interval(*interval_for_overlap)
        benchmark(crabtree_tree.overlaps_interval, ct_interval_for_overlap)


@pytest.mark.benchmark(group="overlaps_point")
class TestOverlapsPoint:
    def test_intervaltree(self, benchmark, intervaltree_tree, point_for_at):
        benchmark(intervaltree_tree.overlaps, point_for_at)

    def test_crabtree(self, benchmark, crabtree_tree, point_for_at):
        benchmark(crabtree_tree.overlaps_point, point_for_at)