from fxkk import levenshtein
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


def test_levenshtein_performance_shared_fixes(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases_shared:
            levenshtein(a, b)

    benchmark(profile_levenshtein)


def test_jellyfish_performance_shared_fixes(benchmark: Any) -> None:
    def profile_levenshtein() -> None:
        for a, b in cases_shared:
            jellyfish_compiled(a, b)

    benchmark(profile_levenshtein)
