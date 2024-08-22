use std::vec;

use pyo3::prelude::*;
use unicode_segmentation::UnicodeSegmentation;
use smallvec::{SmallVec, smallvec};

/// Formats the sum of two numbers as string.
#[pyfunction]
fn levenshtein_mat(a: &str, b: &str) -> PyResult<usize> {
    if a == b {
        return Ok(0)
    }
    let a = UnicodeSegmentation::graphemes(a, true).collect::<Vec<&str>>();
    let b = UnicodeSegmentation::graphemes(b, true).collect::<Vec<&str>>();
    let l_a: usize = a.len() + 1;
    let l_b: usize = b.len() + 1;
    let mut D: Vec<Vec<usize>> = vec![];
    for _ in 0..l_a {
        D.push(vec![0; l_b])
    }
    for i in 1..l_a {
        D[i][0] = i;
    }
    for j in 1..l_b {
        D[0][j] = j;
    }
    let mut cost: usize;
    for i in 1..l_a {
        let a_i = a[i -1];
        for j in 1..l_b {
            let b_j = b[j - 1];
            cost = if a_i == b_j { 0 } else { 1 };
            D[i][j] = std::cmp::min(
                D[i - 1][j] + 1,
                std::cmp::min(
                    D[i][j - 1] + 1, 
                    D[i - 1][j - 1] + cost
                ),
            );
        }
    }
    Ok(D[l_a - 1][l_b - 1])
}

#[pyfunction]
fn levenshtein_vec(a: &str, b: &str) -> PyResult<usize> {
    if a == b {
        return Ok(0)
    }
    let a: Vec<&str> = UnicodeSegmentation::graphemes(a, true).collect::<Vec<&str>>();
    let b: Vec<&str> = UnicodeSegmentation::graphemes(b, true).collect::<Vec<&str>>();
    let l_a: usize = a.len() + 1;
    let l_b: usize = b.len() + 1;
    let mut v_0: Vec<usize> = vec![0; l_b];
    let mut v_1: Vec<usize> = (0..l_b).collect();
    for i in 1..l_a {
        v_0 = v_1;
        v_1 =vec![0; l_b];
        v_1[0] = i;
        for j in 1..l_b {
            let cost: usize = if a[i - 1] == b[j - 1] { 0 } else { 1 };
            v_1[j] = std::cmp::min(
                v_0[j] + 1,
                std::cmp::min(
                    v_1[j - 1] + 1,
                    v_0[j - 1] + cost
                )
            );
        }
    }
    Ok(v_1[l_b - 1])
}

#[inline(always)]
fn levenshtein_exp(a: &[&str], b: &[&str]) -> PyResult<usize> {
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
fn levenshtein_tweaked(a: &str, b: &str) -> PyResult<usize> {
    if b.len() > a.len() {
        return levenshtein_tweaked(b, a);
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
    levenshtein_exp(&source, &target)
}


/// A Python module implemented in Rust.
#[pymodule]
fn fxkk(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(levenshtein_mat, m)?)?;
    m.add_function(wrap_pyfunction!(levenshtein_vec, m)?)?;
    m.add_function(wrap_pyfunction!(levenshtein_tweaked, m)?)?;
    Ok(())
}




#[cfg(test)]
mod tests {

	#[test]
	fn test_tweaked() {
        let a = "kitten";
        let b = "sitting";
        assert_eq!(super::levenshtein_tweaked(a, b).unwrap(), 3);
	}
}

	