from intervaltree import Interval

class TestOverlaps:
    def test_when_a_contains_b(self):
        a = Interval(1, 10)
        b = Interval(2, 8)
        assert a.overlaps(b) == True

    def test_when_a_overlaps_b_on_the_right(self):
        a = Interval(1, 10)
        b = Interval(2, 12)
        assert a.overlaps(b) == True

    def test_when_a_overlaps_b_on_the_left(self):
        a = Interval(2, 12)
        b = Interval(1, 5)
        assert a.overlaps(b) == True

    def test_when_a_is_contained_in_b(self):
        a = Interval(2, 3)
        b = Interval(1, 5)
        assert a.overlaps(b) == True

    def test_when_a_is_before_b(self):
        a = Interval(2, 3)
        b = Interval(4, 5)
        assert a.overlaps(b) == False

    def test_when_a_is_after_b(self):
        a = Interval(4, 5)
        b = Interval(2, 3)
        assert a.overlaps(b) == False