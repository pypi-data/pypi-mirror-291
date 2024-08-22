from fxkk import levenshtein
from jellyfish import levenshtein_distance as jellyfish_compiled
from typing import Any
import random
import string


def random_string(n: int = 10) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


cases = [(random_string(), random_string()) for _ in range(1000)]


def test_levenshtein_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            levenshtein(a, b)

    benchmark(profile_levenshtein)


def test_jellyfish_compiled_performance(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases:
            jellyfish_compiled(a, b)

    benchmark(profile_levenshtein)
