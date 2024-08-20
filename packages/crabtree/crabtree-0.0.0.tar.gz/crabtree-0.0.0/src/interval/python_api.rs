use pyo3::prelude::*;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hasher, Hash};
use crate::interval::interval::Interval;


#[pymethods]
impl Interval {
    #[new]
    fn new(start: i32, end: i32) -> Self {
        match (start, end) {
            (s, e) if s < e => Self { start: start, end: end },
            _ => Self { start: end, end: start }
        }
    }

    fn __eq__(&self, other: &Self) -> bool {
        self.start == other.start && self.end == other.end
    }

    fn __repr__(&self) -> String {
        format!("Interval({}, {})", self.start, self.end)
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        (self.start, self.end).hash(&mut hasher);
        hasher.finish()
    }
}