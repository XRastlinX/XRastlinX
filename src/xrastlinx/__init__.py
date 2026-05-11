"""XRastlinX Mark 1 Review Instrument public API."""

__version__ = "0.1.0"

__all__ = [
    "ALPHA",
    "ALPHA_INV",
    "MARK1_H",
    "MATCH_THRESHOLD",
    "OMEGA_C",
    "PROVEN_PHYSICS",
    "REFUSED_NUMERIC_MISMATCH",
    "UNRESOLVED_REVIEW",
    "Mark1Attractor",
    "RelationshipResult",
    "ShellClosureResult",
    "evaluate_mark1_relations",
    "__version__",
]


def __getattr__(name: str):
    """Lazily expose public Mark 1 helpers without preloading CLI modules."""

    if name in __all__ and name != "__version__":
        from . import mark1

        return getattr(mark1, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
