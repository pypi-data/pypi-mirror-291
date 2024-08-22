# type: ignore
from typing import List
import array as arrayModule


def levenshtein_mat_py(a: str, b: str) -> int:
    """Calculate the Levenshtein distance between two strings."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    l_a = len(a) + 1
    l_b = len(b) + 1
    if l_a == 0:
        return l_b
    if l_b == 0:
        return l_a
    if a == b:
        return 0

    D: List[List[int]] = []
    for i in range(l_a):
        D.append([0] * l_b)

    for i in range(1, l_a):
        D[i][0] = i

    for j in range(1, l_b):
        D[0][j] = j

    for i in range(1, l_a):
        a_i = a[i - 1]
        for j in range(1, l_b):
            b_j = b[j - 1]
            cost = 0 if a_i == b_j else 1
            D[i][j] = min(
                D[i - 1][j] + 1,  # deletion
                D[i][j - 1] + 1,  # insertion
                D[i - 1][j - 1] + cost,  # substitution
            )
    return D[l_a - 1][l_b - 1]


def jellyfish_levenshtein(s1, s2):
    if s1 == s2:
        return 0
    rows = len(s1) + 1
    cols = len(s2) + 1

    if not s1:
        return cols - 1
    if not s2:
        return rows - 1

    prev = None
    cur = range(cols)
    for r in range(1, rows):
        prev, cur = cur, [r] + [0] * (cols - 1)
        for c in range(1, cols):
            deletion = prev[c] + 1
            insertion = cur[c - 1] + 1
            edit = prev[c - 1] + (0 if s1[r - 1] == s2[c - 1] else 1)
            cur[c] = min(edit, deletion, insertion)

    return cur[-1]


def levenshtein_vec_py(s: str, t: str) -> int:
    if s == t:
        return 0
    if not s:
        return len(t)
    if not t:
        return len(s)

    l_s = len(s) + 1
    l_t = len(t) + 1
    v_0 = None
    v_1 = range(l_t)

    for i in range(1, l_s):
        # Old becomes new, new gets initialized to deletion_length
        v_0, v_1 = v_1, [i] + [0] * (l_t - 1)
        for j in range(1, l_t):
            # Calculate the cost of deleting, inserting, or substituting
            deletion = v_0[j] + 1
            insertion = v_1[j - 1] + 1
            substitution = v_0[j - 1] + (0 if s[i - 1] == t[j - 1] else 1)
            v_1[j] = min(deletion, insertion, substitution)
    return v_1[-1]


def levenshtein_exp_py(s, t):
    # https://turnerj.com/blog/levenshtein-distance-part-2-gotta-go-fast
    if s == t:
        return 0
    if not s:
        return len(t)
    if not t:
        return len(s)
    previous_row = arrayModule.array("I", [1] * (len(t) + 1))
    for i in range(1, len(s) + 1):
        previous_diagonal = i - 1
        previous_column = i
        sourceChar = s[i - 1]
        for j in range(1, len(t) + 1):
            local_cost = previous_diagonal
            deletion_cost = previous_row[j]
            if sourceChar != t[j - 1]:
                local_cost = min(local_cost, deletion_cost, previous_column) + 1
            previous_column = local_cost
            previous_row[j] = local_cost
            previous_diagonal = deletion_cost
    return previous_row[-1]


def levenshtein_exp_with_arr(s, t):
    # https://turnerj.com/blog/levenshtein-distance-part-2-gotta-go-fast
    if s == t:
        return 0
    if not s:
        return len(t)
    if not t:
        return len(s)
    previous_row = arrayModule.array("I", range(len(t) + 1))
    for i in range(1, len(s) + 1):
        previous_diagonal = i - 1
        previous_column = previous_diagonal + 1
        sourceChar = s[i - 1]
        for j in range(1, len(t) + 1):
            local_cost = previous_diagonal
            deletion_cost = previous_row[j]
            if sourceChar != t[j - 1]:
                local_cost = min(local_cost, deletion_cost, previous_column) + 1
            previous_column = local_cost
            previous_row[j] = local_cost
            previous_diagonal = deletion_cost
    return previous_row[-1]


def levenshtein_turner(s, t):
    # https://turnerj.com/blog/levenshtein-distance-part-2-gotta-go-fast
    if s == t:
        return 0
    if not s:
        return len(t)
    if not t:
        return len(s)
    previous_row = list(range(len(t) + 1))
    for i in range(1, len(s) + 1):
        previous_diagonal = i - 1
        previous_column = previous_diagonal + 1
        sourceChar = s[i - 1]
        for j in range(1, len(t) + 1):
            local_cost = previous_diagonal
            deletion_cost = previous_row[j]
            if sourceChar != t[j - 1]:
                local_cost = min(local_cost, deletion_cost, previous_column) + 1
            previous_column = local_cost
            previous_row[j] = local_cost
            previous_diagonal = deletion_cost
    return previous_row[-1]


def levenshtein_exp_backup(s, t):
    # https://turnerj.com/blog/levenshtein-distance-part-2-gotta-go-fast
    if s == t:
        return 0
    if not s:
        return len(t)
    if not t:
        return len(s)
    previous_row = list(range(len(t) + 1))
    for i in range(1, len(s) + 1):
        previous_diagonal = i - 1
        previous_column = previous_diagonal + 1
        sourceChar = s[i - 1]
        for j in range(1, len(t) + 1):
            if sourceChar == t[j - 1]:
                previous_column = previous_diagonal
            else:
                previous_column = (
                    min(previous_column, previous_diagonal, previous_row[j]) + 1
                )
            previous_diagonal = previous_row[j]
            previous_row[j] = previous_column
    return previous_row[-1]
