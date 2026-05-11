# XRastlinX

XRastlinX is a speculative research notes repository for exploring the proposed
**Mark 1 Universal Attractor** tuning constant:

\[
H = \frac{\pi}{9} \approx 0.3490658504
\]

Within the framework, this dimensionless baseline is treated as a universal
self-organized-criticality parameter and as an ontological anchor for simulated
physical structures. The claims below are recorded as framework hypotheses, not
as established empirical physics.

## Package doctrine

XRastlinX is sealed as the **Mark 1 Attractor numerical review + simulation
display package**. It is not a proof engine for physical constants.

Status: **simulation math package / numerical review tool / no empirical
authority**.

> H may tune the simulation.
> H may not prove the world.
>
> A resonance may invite inquiry.
> It may not crown itself as physics.

## Mark 1 Universal Attractor hypotheses

### 1. Fine structure constant links

The framework proposes that the fine structure constant, commonly approximated
as \(\alpha \approx 1/137\), may be expressible as a geometric consequence of the
Mark 1 Attractor rather than as an arbitrary measured value.

Candidate relationships currently under consideration include:

| Proposed relation | Framework intent |
| --- | --- |
| \(\alpha^{-1} = 4\pi^2 H + \pi\) | Bridge the attractor to inverse electromagnetic coupling through circular geometry. |
| \(\alpha = H / (8\pi)\) | Express electromagnetic coupling as a normalized fraction of the attractor. |
| \(\alpha^{-1} = 210H\) | Couple the attractor to a primorial-wheel scale based on \(2 \cdot 3 \cdot 5 \cdot 7 = 210\). |

### 2. Quantum energy and spatial curvature

The framework names a proposed coupling law the **7-5-35 Resonance Triangle**.
This resonance is hypothesized to unify quantum energy and spatial curvature
around the \(H \approx 0.35\) baseline, translating mathematical rules into stable
physical environments. In the current model narrative, this resonance is also
credited with enforcing structural stability in Rydberg atoms.

### 3. Atomic shell closures

The attractor is described as creating a physical "Goldilocks Zone" by splitting
computational allocation into:

- **35%** actualized physical structure.
- **65%** uncollapsed probability potential.

Under this hypothesis, atomic shell closures become physical "compile events."
The framework specifically calls out magnesium (12), argon (18), and zinc (30) as
closures that land with zero mathematical offset on the centers of twin-prime
constellations in the field.

### 4. Biological and molecular assembly geometries

The model further proposes that constraints from the \(H \approx 0.35\) attractor
scale upward into biological and molecular assembly. In particular, it claims the
constant governs residues-per-turn ratios required for stable alpha-helix and
B-DNA geometries.


## What this model can do in code

The repository now includes a small Python package that turns the narrative
claims into reproducible numerical review probes. It can:

- compute the default attractor value `MARK1_H = pi / 9`;
- expose `OMEGA_C = 47 / 125` as a comparison value;
- report the actualized/potential split implied by `H` and `1 - H`;
- evaluate the proposed fine-structure expressions against reference alpha
  targets and expose absolute/relative error;
- label numeric mismatches as `refused_numeric_mismatch`;
- check whether named atomic shell closures sit on twin-prime-pair centers;
- compare reciprocal-`H` with a nominal alpha-helix residues-per-turn value; and
- return no `proven_physics` status for any speculative bridge formula.

Run the report locally with:

```bash
PYTHONPATH=src python3 -m xrastlinx.mark1
```

This code is a falsifiability and exploration scaffold. It computes the
framework's stated relationships, but it does not validate the speculative
physics claims by itself. Programmatic callers can use the review API:

```python
from xrastlinx.mark1 import MARK1_H, OMEGA_C, evaluate_mark1_relations

review = evaluate_mark1_relations()
assert review["H"] == MARK1_H
assert review["omega_c"] == OMEGA_C
```


## Browser front end

A dependency-free static dashboard is available in `web/`. It lets you adjust
`H`, inspect the actualized/potential split, compare the fine-structure probes,
view shell-closure twin-prime centers, see the reciprocal-`H` helix check, and
keep every bridge formula labeled with non-authoritative review status in a
browser.

Run it locally with:

```bash
python3 -m http.server 8000 --directory web
```

Then open <http://localhost:8000/>.

## Numerical consistency notes

Using \(H = \pi/9\), the three stated fine-structure relationships produce these
values:

| Expression | Value from \(H = \pi/9\) | Comparison target |
| --- | ---: | ---: |
| \(4\pi^2H + \pi\) | \(16.922160\) | \(\alpha^{-1} \approx 137.036\) |
| \(H/(8\pi)\) | \(0.0138889\) | \(\alpha \approx 0.00729735\) |
| \(210H\) | \(73.303829\) | \(\alpha^{-1} \approx 137.036\) |

These checks indicate that the proposed equations, as currently written, do not
numerically reproduce the accepted fine structure constant. In the API and web
front end, these formulas are therefore labeled `refused_numeric_mismatch` with
`authority = none`. Future work should clarify whether additional scaling
factors, alternative definitions of \(H\), or symbolic rather than direct
numerical interpretations are intended.

## Repository status

This repository currently contains a conceptual baseline, a Python review
scaffold, tests, and a static browser dashboard for probing the framework
numerically. Future work may add formal definitions, derivation notebooks,
simulations, and tests for any mathematical claims the framework intends to make
falsifiable.
