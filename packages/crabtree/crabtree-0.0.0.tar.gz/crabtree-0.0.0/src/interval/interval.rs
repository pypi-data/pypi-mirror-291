use pyo3::prelude::*;
use std::fmt::{Display, Formatter};
use std::cmp::Ordering;


#[pyclass]
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Hash)]
pub struct Interval {
    #[pyo3(get)]
    pub start: i32,
    #[pyo3(get)]
    pub end: i32
}

impl Interval {
    pub fn overlaps(&self, other: &Self) -> bool {
        self.end > other.start && other.end > self.start
    }

    pub fn contains(&self, point: i32) -> bool {
        self.start <= point && point <= self.end
    }
}


impl Ord for Interval {
    fn cmp(&self, other: &Self) -> Ordering {
        (self.start, self.end).cmp(&(other.start, other.end))
    }
}

impl Display for Interval {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "[{}, {}]", self.start, self.end)
    }
}