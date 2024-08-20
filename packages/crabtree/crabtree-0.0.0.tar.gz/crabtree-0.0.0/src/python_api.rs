use pyo3::prelude::*;

use crate::interval::interval::Interval;
use crate::interval_tree::interval_tree::IntervalTree;


#[pymodule]
fn crabtree(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Interval>()?;
    m.add_class::<IntervalTree>()?;
    Ok(())
}