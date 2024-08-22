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


def random_string(n: int = 10) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


cases = [(random_string(), random_string()) for _ in range(1000)]


def test_levenshtein_mat_rs_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            levenshtein_mat_rs(a, b)

    benchmark(profile_levenshtein)


def test_levenshtein_vec_rs_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            levenshtein_vec_rs(a, b)

    benchmark(profile_levenshtein)


def test_levenshtein_tweaked_rs_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            levenshtein_tweaked_rs(a, b)

    benchmark(profile_levenshtein)


def test_jellyfish_raw_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            jellyfish_raw(a, b)

    benchmark(profile_levenshtein)


def test_jellyfish_compiled_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            jellyfish_compiled(a, b)

    benchmark(profile_levenshtein)


def test_levenshtein_mat_performance(benchmark: Any) -> None:
    def profile_fast_levenshtein() -> None:
        for a, b in cases:
            levenshtein_mat_py(a, b)

    benchmark(profile_fast_levenshtein)


def test_levenshtein_vec_performance(benchmark: Any) -> None:
    def profile_levenshtein_vec() -> None:
        for a, b in cases:
            levenshtein_vec_py(a, b)

    benchmark(profile_levenshtein_vec)


def test_levenshtein_cy_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            levenshtein_cy(a, b)

    benchmark(profile_levenshtein)


def test_levenstein_exp_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            levenshtein_exp_py(a, b)

    benchmark(profile_levenshtein)
