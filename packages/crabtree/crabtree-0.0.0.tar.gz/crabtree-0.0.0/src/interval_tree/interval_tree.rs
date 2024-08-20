use pyo3::prelude::*;
use std::collections::HashSet;
use crate::interval::interval::Interval;
use crate::node::Node;


#[pyclass]
pub struct IntervalTree {
    root: Option<Box<Node>>,
    #[pyo3(get)]
    pub intervals: HashSet<Interval>,
}

pub enum IntervalTreeError {
    IntervalNotFound(Interval)
}

// Construction
impl IntervalTree {
    pub fn new() -> Self {
        IntervalTree { root: None, intervals: HashSet::new() }
    }

    pub fn from_intervals(intervals: Vec<Interval>) -> Self {
        match intervals.as_slice() {
            [] => Self::new(),
            [head, tail @ ..] => {
                let mut tree = Self::new();
                tree.intervals = HashSet::from_iter(intervals.iter().cloned());
                tree.add_rec(head.clone());
                tail.iter().for_each(|i| tree.add_rec(i.clone()));
                tree
            }
        }
    }

    pub fn add_rec(&mut self, interval: Interval) {
        match &mut self.root {
            Some(node) => node.add_rec(&interval),
            None => self.root = Some(Node::new(interval.clone())),
        }
        self.intervals.insert(interval.clone());
        self.balance();
    }

    pub fn overlap_rec(&self, interval: &Interval) -> HashSet<Interval> {
        match &self.root {
            Some(node) => node.overlap_rec(interval),
            None => HashSet::new()
        }
    }

    pub fn at_rec(&self, point: i32) -> HashSet<Interval> {
        match &self.root {
            Some(node) => node.at_rec(point),
            None => HashSet::new()
        }
    }

    pub fn overlaps_interval_rec(&self, interval: &Interval) -> bool {
        match &self.root {
            Some(node) => node.overlaps_interval_rec(interval),
            None => false,
        }
    }

    pub fn overlaps_point_rec(&self, point: i32) -> bool {
        match &self.root {
            Some(node) => node.overlaps_point_rec(point),
            None => false,
        }
    }
}

// Restructuring
impl IntervalTree {
    pub fn merge_overlaps_rec(&mut self) {
        if self.intervals.len() <= 1 {
            return;
        }

        let mut intervals = self.get_sorted_intervals();
        intervals.sort();

        let mut merged_intervals: Vec<Interval> = vec![];
        for current in intervals {
            match &mut merged_intervals.as_mut_slice() {
                &mut [.., last] if current.start <= last.end => last.end = last.end.max(current.end),
                _ => merged_intervals.push(current.clone())
            }
        }

        self.root = None;
        merged_intervals.iter().for_each(|i| self.add_rec(i.clone()));
        self.intervals = HashSet::from_iter(merged_intervals.iter().cloned());
    }

    pub fn balance(&mut self) {
        // TODO
    }
}

// Traversal
impl IntervalTree {
    pub fn get_sorted_intervals(&self) -> Vec<Interval> {
        match &self.root {
            Some(node) => node.get_sorted_intervals_rec(),
            None => vec![],
        }
    }

    pub fn display_rec(&self) {
        match &self.root {
            Some(node) => node.display_rec(0),
            None => println!("empty tree")
        }
    }
}

// Removal
impl IntervalTree {
    pub fn remove_rec(&mut self, interval: &Interval) -> Result<(), IntervalTreeError> {
        self.root = self.root.take().and_then(|root| root.remove_rec(interval));
        Ok(())
    }
}