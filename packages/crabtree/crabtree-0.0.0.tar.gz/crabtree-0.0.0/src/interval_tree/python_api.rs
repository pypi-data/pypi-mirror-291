use std::result::Result;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PySequence;
use std::collections::HashSet;
use crate::interval_tree::interval_tree::IntervalTree;
use crate::interval::interval::Interval;

use super::interval_tree::IntervalTreeError;


#[pymethods]
impl IntervalTree {
    #[new]
    fn init(intervals: &Bound<'_, PySequence>) -> PyResult<Self> {
        let i: Vec<Interval> = intervals.extract()?;
        Ok(IntervalTree::from_intervals(i))
    }

    fn display(&self) {
        self.display_rec()
    }

    fn overlap(&self, interval: &Bound<'_, Interval>) -> PyResult<HashSet<Interval>> {
        let i: Interval = interval.extract()?;
        Ok(self.overlap_rec(&i))
    }

    fn at(&self, point: i32) -> PyResult<HashSet<Interval>> {
        Ok(self.at_rec(point))
    }

    fn merge_overlaps(&mut self) -> PyResult<()> {
        Ok(self.merge_overlaps_rec())
    }

    fn overlaps_interval(&self, interval: &Bound<'_, Interval>) -> PyResult<bool> {
        let i: Interval = interval.extract()?;
        Ok(self.overlaps_interval_rec(&i))
    }

    fn overlaps_point(&self, point: i32) -> PyResult<bool> {
        Ok(self.overlaps_point_rec(point))
    }

    fn contains(&self, point: i32) -> PyResult<bool> {
        Ok(self.overlaps_point_rec(point))
    }

    fn add(&mut self, interval: &Bound<'_, Interval>) -> PyResult<()> {
        let i: Interval = interval.extract()?;
        self.add_rec(i);
        Ok(())
    }

    fn remove(&mut self, interval: &Bound<'_, Interval>) -> PyResult<()> {
        let i: Interval = interval.extract()?;
        match self.remove_rec(&i) {
            Result::Ok(()) => Ok(()),
            Result::Err(IntervalTreeError::IntervalNotFound(_)) => 
                Err(PyValueError::new_err(format!("interval not found: {}", i)))
        }
    }

    fn sorted_intervals(&self) -> PyResult<Vec<Interval>> {
        Ok(self.get_sorted_intervals())
    }

    fn __repr__(&self) -> String {
        let intervals = Vec::from_iter(&self.intervals)
            .into_iter()
            .map(|i| format!("{}", i))
            .collect::<Vec<String>>()
            .join(", ");
        format!("IntervalTree({})", intervals)
    }
}