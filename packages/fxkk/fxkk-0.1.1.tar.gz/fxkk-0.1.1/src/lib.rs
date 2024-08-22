use std::vec;

use pyo3::prelude::*;
use unicode_segmentation::UnicodeSegmentation;

#[inline(always)]
fn _levenshtein(a: &[&str], b: &[&str]) -> PyResult<usize> {
    let mut row: Vec<usize> = (1..b.len()+1).collect();
    let mut previous_diagonal: usize;
    let mut cost: usize;
    let mut previous_row: usize = 0;
    for (i, c_a) in a.iter().enumerate() {
        previous_row = i + 1;
        let mut previous_above = i;
        for (j, c_b) in b.iter().enumerate() {
            cost = if c_a == c_b { 0 } else { 1 };
            previous_diagonal = previous_above;
            previous_above = row[j];
            previous_row = std::cmp::min(previous_diagonal+cost, // Substitution 
                std::cmp::min(
                    previous_above+1, // Deletion
                    previous_row+1 // Insertion
                )
            );
            row[j] = previous_row;
        }
    } 

    Ok(previous_row)   
}

/// Find the length of a common prefix of two strings
fn mismatch(a: &[&str], b: &[&str]) -> usize {
    let mut i = 0;
    for (c_a, c_b) in a.iter().zip(b.iter()) {
        if c_a != c_b {
            break;
        }
        i += 1;
    }
    i
}

#[pyfunction]
fn levenshtein(a: &str, b: &str) -> PyResult<usize> {
    if b.len() > a.len() {
        return levenshtein(b, a);
    }
    if a.is_empty() {
        return Ok(b.len());
    }
    if b.is_empty() {
        return Ok(a.len());
        
    }
    if a == b {
        return Ok(0)
    }
    let mut source: Vec<&str>;
    let mut target: Vec<&str>;
    if !a.is_ascii() || !b.is_ascii() {
        source = UnicodeSegmentation::graphemes(a, true).collect::<Vec<&str>>();
        target = UnicodeSegmentation::graphemes(b, true).collect::<Vec<&str>>();
    } else {
        source = a.split("").collect::<Vec<&str>>();
        target= b.split("").collect::<Vec<&str>>();
    }
    let prefix_len = mismatch(&source, &target);
    source.drain(0..prefix_len);
    target.drain(0..prefix_len);
    source.reverse();
    target.reverse();
    let suffix_len = mismatch(&source, &target);
    source.drain(0..suffix_len);
    target.drain(0..suffix_len);
    _levenshtein(&source, &target)
}


/// A Python module implemented in Rust.
#[pymodule]
fn fxkk(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(levenshtein, m)?)?;
    Ok(())
}




#[cfg(test)]
mod tests {

	#[test]
	fn test_tweaked() {
        let a = "kitten";
        let b = "sitting";
        assert_eq!(super::levenshtein(a, b).unwrap(), 3);
	}
}

	