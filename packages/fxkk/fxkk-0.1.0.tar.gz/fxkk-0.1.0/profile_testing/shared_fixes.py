from fxkk import (
    levenshtein_mat_py,
    levenshtein_vec_py,
    levenshtein_exp_py,
    jellyfish_levenshtein as jellyfish_raw,
    levenshtein_cy,
    levenshtein_mat_rs,
    levenshtein_vec_rs,
    levenshtein_tweaked_rs,
)
from jellyfish import levenshtein_distance as jellyfish_compiled
from typing import Any
import random
import string


def random_string_shared_fixes(n: int = 10) -> str:
    return (
        "gillespie "
        + "".join(random.choice(string.ascii_letters) for _ in range(n))
        + " theorem"
    )


cases_shared = [
    (random_string_shared_fixes(), random_string_shared_fixes()) for _ in range(1000)
]


def test_levenshtein_tweaked_rs_performance_shared_fixes(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases_shared:
            levenshtein_tweaked_rs(a, b)

    benchmark(profile_levenshtein)


def test_jellyfish_performance_shared_fixes(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases_shared:
            jellyfish_compiled(a, b)

    benchmark(profile_levenshtein)
