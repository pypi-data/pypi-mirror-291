# type: ignore
import cython
from cython.cimports.cpython import array


def levenshtein(s: str, t: str) -> int:
    # https://turnerj.com/blog/levenshtein-distance-part-2-gotta-go-fast
    previous_diagonal: cython.uint
    previous_column: cython.uint
    local_cost: cython.uint
    deletion_cost: cython.uint
    i: cython.uint
    j: cython.uint
    if s == t:
        return 0
    l_s: cython.uint = len(s)
    l_t: cython.uint = len(t)
    if l_s == 0:
        return l_t
    if l_t == 0:
        return l_s
    previous_row: cython.uint[:] = array.array("I", range(l_t + 1))
    for i in range(1, l_s + 1):
        previous_diagonal = i - 1
        previous_column = previous_diagonal + 1
        with cython.boundscheck(False), cython.wraparound(False):
            sourceChar = s[i - 1]
        for j in range(1, l_t + 1):
            local_cost = previous_diagonal
            deletion_cost = previous_row[j]
            if sourceChar != t[j - 1]:
                local_cost = min(local_cost, deletion_cost, previous_column) + 1
            previous_column = local_cost
            previous_row[j] = local_cost
            previous_diagonal = deletion_cost
    return previous_row[j]
