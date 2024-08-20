use std::collections::HashSet;
    use crate::interval::interval::Interval;


pub struct Node {
    pub interval: Interval,
    pub left: Option<Box<Node>>,
    pub right: Option<Box<Node>>,
    max_value: i32,
}

impl Node {
    pub fn new(interval: Interval) -> Box<Self> {
        let max_value = interval.end;
        Box::new(Node {
            interval,
            max_value,
            left: None,
            right: None
        })
    }

    pub fn add_rec(&mut self, interval: &Interval) {
        if interval < &self.interval {
            match &mut self.left {
                Some(child) => child.add_rec(interval),
                None => self.left = Some(Node::new(interval.clone()))
            }
        }
        else if &self.interval < interval {
            match &mut self.right {
                Some(child) => child.add_rec(interval),
                None => self.right = Some(Node::new(interval.clone()))
            }
        }
        if &self.max_value < &interval.end {
            self.max_value = interval.end;
        }
    }

    pub fn overlap_rec(&self, interval: &Interval) -> HashSet<Interval> {
        if self.max_value < interval.start {
            return HashSet::new();
        }
        if interval.end < self.interval.start {
            return match &self.left {
                Some(node) => node.overlap_rec(interval),
                None => HashSet::new()
            }
        }
        
        let mut overlap = HashSet::new();
        if interval.overlaps(&self.interval) {
            overlap.insert(self.interval.clone());
        }
        overlap = match &self.left {
            Some(node) => &overlap | &node.overlap_rec(interval),
            None => overlap
        };
        overlap = match &self.right {
            Some(node) => &overlap | &node.overlap_rec(interval),
            None => overlap
        };

        overlap
    }

    pub fn at_rec(&self, point: i32) -> HashSet<Interval> {
        if self.max_value < point {
            return HashSet::new();
        }
        if point < self.interval.start {
            return match &self.left {
                Some(node) => node.at_rec(point),
                None => HashSet::new()
            }
        } 

        let mut overlap = HashSet::new();
        if self.interval.contains(point) {
            overlap.insert(self.interval.clone());
        }
        overlap = match &self.left {
            Some(node) => &overlap | &node.at_rec(point),
            None => overlap
        };
        overlap = match &self.right {
            Some(node) => &overlap | &node.at_rec(point),
            None => overlap
        };

        overlap
    }

    pub fn get_sorted_intervals_rec(&self) -> Vec<Interval> {
        let mut sorted_intervals = vec![];
        match &self.left {
            Some(node) => sorted_intervals.append(&mut node.get_sorted_intervals_rec()),
            None => {}
        };
        sorted_intervals.push(self.interval.clone());
        match &self.right {
            Some(node) => sorted_intervals.append(&mut node.get_sorted_intervals_rec()),
            None => {}
        };

        sorted_intervals
    }

    pub fn overlaps_interval_rec(&self, interval: &Interval) -> bool {
        if interval.overlaps(&self.interval) {
            return true;
        }

        if self.max_value < interval.start {
            return false;
        }

        if interval.end < self.interval.start {
            return match &self.left {
                Some(node) => node.overlaps_interval_rec(interval),
                None => false
            }
        }

        match &self.right {
            Some(node) => node.overlaps_interval_rec(interval),
            None => false
        }
    }

    pub fn overlaps_point_rec(&self, point: i32) -> bool {
        if self.interval.contains(point) {
            return true;
        }

        if self.max_value < point {
            return false;
        }

        if point < self.interval.start {
            return match &self.left {
                Some(node) => node.overlaps_point_rec(point),
                None => false
            }
        }

        match &self.right {
            Some(node) => node.overlaps_point_rec(point),
            None => false
        }
    }

    pub fn display_rec(&self, indent: usize) {
        let indent_spaces = " ".repeat(indent);
        println!("{}([{}, {}], {})", indent_spaces, self.interval.start, self.interval.end, self.max_value);
        match &self.left {
            Some(child) => child.display_rec(indent + 4),
            None => {}
        }
        match &self.right {
            Some(child) => child.display_rec(indent + 4),
            None => {}
        }
    }
}


// Removal
impl Node {
    // TODO: This is 10x slower than Python version, find why
    pub fn remove_rec(mut self: Box<Node>, interval: &Interval) -> Option<Box<Self>> {
        if self.interval.cmp(interval).is_eq() {
            return match (self.left.take(), self.right.take()) {
                (None, None) => None,
                (left @ Some(_), None) => left,
                (None, right @ Some(_)) => right,
                (Some(mut left), Some(right)) => {
                    if let Some(mut predecessor) = left.find_rightmost_child() {
                        predecessor.right = Some(right);
                        predecessor.left = Some(left);
                        Some(predecessor)
                    } else {
                        left.right = Some(right);
                        Some(left)
                    }
                }
            }
        }

        let (dig_left, dig_right) = self.dig_directions(interval);
        if dig_left {
            self.left = self.left.and_then(|node| node.remove_rec(interval));
        }
        if dig_right {
            self.right = self.right.and_then(|node| node.remove_rec(interval));
        }

        Some(self)
    }

    fn find_rightmost_child(&mut self) -> Option<Box<Self>> {
        match self.right {
            Some(ref mut right) => {
                if let Some(node) = right.find_rightmost_child() {
                    Some(node)
                } else {
                    let mut node = self.right.take();
                    if let Some(ref mut node) = node {
                        self.right = std::mem::replace(& mut node.left, None);
                    }
                    node
                }
            },
            None => None
        }
    }
}

// Traversal
impl Node {
    pub fn dig(&self, interval: &Interval) -> Vec<&Box<Self>> {
        let mut children_to_dig = vec![];
        let (dig_left, dig_right) = self.dig_directions(interval);
        if dig_left {
            if let Some(child) = &self.left {
                children_to_dig.push(child)
            }
        }
        if dig_right {
            if let Some(child) = &self.right {
                children_to_dig.push(child)
            }
        }

        children_to_dig
    }

    pub fn dig_directions(&self, interval: &Interval) -> (bool, bool) {
        let mut dig_left = true;
        let mut dig_right = true;
        if interval.end < self.interval.start {
            dig_right = false;
        }
        if self.max_value < interval.start {
            dig_left = false;
            dig_right = false;
        }
        (dig_left, dig_right)
    }
}