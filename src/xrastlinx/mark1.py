"""Truth-preserving probes for the speculative Mark 1 Attractor model.

XRastlinX is a numerical review instrument, not empirical authority. The code
records candidate relationships, computes their values, and labels mismatches so
that speculative bridges cannot silently masquerade as proven physics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import math
from typing import Callable, Iterable, Literal, TypedDict

MARK1_H = math.pi / 9
OMEGA_C = 47 / 125
ALPHA = 7.297_352_5693e-3
ALPHA_INV = 137.035_999_084
MATCH_THRESHOLD = 1e-3
PROVEN_PHYSICS = "proven_physics"
REFUSED_NUMERIC_MISMATCH = "refused_numeric_mismatch"
UNRESOLVED_REVIEW = "unresolved_review"

ReviewStatus = Literal["refused_numeric_mismatch", "unresolved_review", "proven_physics"]


class Mark1Review(TypedDict):
    """Dictionary shape returned by :func:`evaluate_mark1_relations`."""

    H: float
    omega_c: float
    status: str
    authority: str
    relations: list[dict[str, object]]


@dataclass(frozen=True)
class RelationshipResult:
    """A numerical result for a proposed relationship."""

    name: str
    expression: str
    value: float
    target: float
    absolute_error: float
    relative_error: float
    status: ReviewStatus
    authority: str
    notes: str

    @property
    def matches_target(self) -> bool:
        """Return True when the value is close enough for exploratory reporting."""

        return self.relative_error <= MATCH_THRESHOLD

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-friendly representation for APIs and displays."""

        return asdict(self)


@dataclass(frozen=True)
class ShellClosureResult:
    """A shell closure candidate and its distance from a twin-prime center."""

    element: str
    atomic_number: int
    nearest_twin_prime_pair: tuple[int, int]
    twin_prime_center: float
    offset: float
    status: ReviewStatus = UNRESOLVED_REVIEW
    authority: str = "none"

    @property
    def is_centered(self) -> bool:
        """Return True when the closure is exactly centered on a twin-prime pair."""

        return self.offset == 0


class Mark1Attractor:
    """Numerical facade for Mark 1 Attractor review probes."""

    def __init__(self, h: float = MARK1_H, omega_c: float = OMEGA_C) -> None:
        self.h = h
        self.omega_c = omega_c

    @property
    def actualized_fraction(self) -> float:
        """Fraction of the model allocated to actualized structure."""

        return self.h

    @property
    def potential_fraction(self) -> float:
        """Complementary uncollapsed probability-potential fraction."""

        return 1 - self.h

    def fine_structure_relationships(self) -> list[RelationshipResult]:
        """Evaluate proposed fine-structure relationships against alpha targets."""

        candidates: list[tuple[str, str, Callable[[], float], float, str]] = [
            (
                "circular inverse-alpha bridge",
                "4*pi^2*H + pi",
                lambda: 4 * math.pi**2 * self.h + math.pi,
                ALPHA_INV,
                "Candidate inverse-alpha bridge through circular geometry.",
            ),
            (
                "normalized alpha fraction",
                "H / (8*pi)",
                lambda: self.h / (8 * math.pi),
                ALPHA,
                "Candidate alpha expression as a normalized fraction of the attractor.",
            ),
            (
                "primorial-wheel inverse-alpha bridge",
                "210*H",
                lambda: 210 * self.h,
                ALPHA_INV,
                "Candidate coupling to the 2*3*5*7 primorial-wheel scale.",
            ),
        ]
        return [self._relationship_result(*candidate) for candidate in candidates]

    def shell_closure_offsets(
        self,
        closures: Iterable[tuple[str, int]] = (("Magnesium", 12), ("Argon", 18), ("Zinc", 30)),
    ) -> list[ShellClosureResult]:
        """Compare shell closures to the nearest twin-prime-pair centers.

        A twin-prime center is the midpoint of a pair `(p, p + 2)`. Exact integer
        centers therefore occur at integer values such as 4, 6, 12, 18, and 30 for
        pairs `(3, 5)`, `(5, 7)`, `(11, 13)`, `(17, 19)`, and `(29, 31)`.
        """

        closure_list = list(closures)
        max_atomic_number = max(number for _, number in closure_list)
        twin_pairs = list(self._twin_prime_pairs(max_atomic_number + 4))
        results: list[ShellClosureResult] = []
        for element, atomic_number in closure_list:
            nearest_pair = min(
                twin_pairs,
                key=lambda pair: abs(atomic_number - self._pair_center(pair)),
            )
            center = self._pair_center(nearest_pair)
            results.append(
                ShellClosureResult(
                    element=element,
                    atomic_number=atomic_number,
                    nearest_twin_prime_pair=nearest_pair,
                    twin_prime_center=center,
                    offset=atomic_number - center,
                )
            )
        return results

    def helix_turn_estimate(self, residues_per_turn: float = 3.6) -> RelationshipResult:
        """Compare a residue-turn ratio with the attractor reciprocal scale."""

        value = 1 / self.h
        return self._relationship_result(
            name="alpha-helix reciprocal-H comparison",
            expression="1/H",
            evaluate=lambda: value,
            target=residues_per_turn,
            notes="Compares reciprocal-H to a nominal alpha-helix residues-per-turn value.",
        )

    def review(self) -> Mark1Review:
        """Return the doctrinal review payload for programmatic consumers."""

        relations = [result.as_dict() for result in self.fine_structure_relationships()]
        relations.append(self.helix_turn_estimate().as_dict())
        return {
            "H": self.h,
            "omega_c": self.omega_c,
            "status": UNRESOLVED_REVIEW,
            "authority": "none",
            "relations": relations,
        }

    def summary(self) -> str:
        """Render a compact human-readable model report."""

        lines = [
            "Mark 1 Review Instrument computational report",
            f"H = {self.h:.10f}",
            f"omega_c = {self.omega_c:.6f}",
            f"actualized_fraction = {self.actualized_fraction:.6f}",
            f"potential_fraction = {self.potential_fraction:.6f}",
            "authority = none",
            "",
            "Fine-structure probes:",
        ]
        for result in self.fine_structure_relationships():
            lines.append(
                f"- {result.expression}: {result.value:.9g} vs {result.target:.9g} "
                f"(status={result.status}; rel_err={result.relative_error:.3%})"
            )

        lines.extend(["", "Shell-closure probes:"])
        for result in self.shell_closure_offsets():
            lines.append(
                f"- {result.element} ({result.atomic_number}) -> twin prime "
                f"{result.nearest_twin_prime_pair}, center={result.twin_prime_center:g}, "
                f"offset={result.offset:g}, status={result.status}"
            )

        helix = self.helix_turn_estimate()
        lines.extend(
            [
                "",
                "Biological-geometry probe:",
                f"- {helix.expression}: {helix.value:.9g} vs {helix.target:.9g} "
                f"(status={helix.status}; rel_err={helix.relative_error:.3%})",
                "",
                "No relation is labeled proven_physics.",
            ]
        )
        return "\n".join(lines)

    def _relationship_result(
        self,
        name: str,
        expression: str,
        evaluate: Callable[[], float],
        target: float,
        notes: str,
    ) -> RelationshipResult:
        value = evaluate()
        absolute_error = abs(value - target)
        relative_error = absolute_error / abs(target)
        status: ReviewStatus = UNRESOLVED_REVIEW if relative_error <= MATCH_THRESHOLD else REFUSED_NUMERIC_MISMATCH
        return RelationshipResult(
            name=name,
            expression=expression,
            value=value,
            target=target,
            absolute_error=absolute_error,
            relative_error=relative_error,
            status=status,
            authority="none",
            notes=notes,
        )

    @staticmethod
    def _pair_center(pair: tuple[int, int]) -> float:
        return (pair[0] + pair[1]) / 2

    @classmethod
    def _twin_prime_pairs(cls, maximum: int) -> Iterable[tuple[int, int]]:
        primes = {number for number in range(2, maximum + 1) if cls._is_prime(number)}
        for prime in sorted(primes):
            if prime + 2 in primes:
                yield (prime, prime + 2)

    @staticmethod
    def _is_prime(number: int) -> bool:
        if number < 2:
            return False
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        limit = int(math.sqrt(number)) + 1
        return all(number % divisor for divisor in range(3, limit, 2))


def evaluate_mark1_relations(h: float = MARK1_H, omega_c: float = OMEGA_C) -> Mark1Review:
    """Evaluate Mark 1 review relations as a JSON-friendly dictionary."""

    return Mark1Attractor(h=h, omega_c=omega_c).review()


def main() -> None:
    """Run the Mark 1 review report from the command line."""

    parser = argparse.ArgumentParser(description="Run Mark 1 Attractor review probes.")
    parser.add_argument("--h", type=float, default=MARK1_H, help="Attractor value to evaluate.")
    parser.add_argument("--omega-c", type=float, default=OMEGA_C, help="Omega-c comparison value to report.")
    args = parser.parse_args()
    print(Mark1Attractor(h=args.h, omega_c=args.omega_c).summary())


if __name__ == "__main__":
    main()
