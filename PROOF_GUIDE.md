# Reading the cocompact proof

The entry point is
[`FuchsianCocompactSingularity.lean`](Singularity/FuchsianCocompactSingularity.lean).
Its theorem `cocompact_fuchsian_hittingMeasure_singular` concerns the actual
hitting measure of the original PSL₂ random walk. The neighboring declaration
`cocompact_fuchsian_hittingMeasure_singular_lebesgue` gives the real-chart
Lebesgue formulation.

## 1. Projective formulation and the lifted walk

[`ProjectiveNonelementary.lean`](Singularity/ProjectiveNonelementary.lean)
defines nonelementarity using finite geometric orbits and derives infinitude
of every boundary orbit.

[`ProjectiveCocompactSingularity.lean`](Singularity/ProjectiveCocompactSingularity.lean)
passes to the full inverse image of Γ in SL₂. Each supported projective jump
is lifted with both signs, each assigned half its original weight. The lift
is discrete and cocompact, its support generates the lifted group, and its
projected hitting measure agrees with the original one. The spectral gap is
proved from the geometric hypotheses.

## 2. Reduce failure of singularity to absolute continuity

[`CocompactHittingSingularity.lean`](Singularity/CocompactHittingSingularity.lean)
contains the main contradiction argument in SL₂. The hitting-measure zero–one
law shows that failure of singularity implies visual absolute continuity of
the forward hitting measure.

## 3. Obtain the reflected absolute continuity without symmetry

[`OneSidedNaimRigidity.lean`](Singularity/OneSidedNaimRigidity.lean) proves
that forward visual absolute continuity identifies the actual invariant
Naïm quotient probability with Haar probability. Its supporting modules
construct the Naïm measure, descend it to the compact quotient, and transfer
stable average basins using the forward marginal's absolute continuity.
This yields visual absolute continuity of the reflected hitting measure.
It does not assume that the original random walk is symmetric.

## 4. Apply the two-sided Fourier obstruction

[`CocompactTwoSidedSingularity.lean`](Singularity/CocompactTwoSidedSingularity.lean)
proves that the forward and reflected measures cannot both have the required
absolute continuity. Its dependency chain includes the Green and compressed
Green operators, separator identities, boundary limits, the invariant-current
comparison, and the Fourier obstruction for finitely generated lattice
translate families.

The contradiction in step 2 proves forward singularity. Applying the same
argument to the reflected law also proves reflected singularity.

## 5. Return to the original hitting law and Lebesgue measure

The projective lifting identities transfer the conclusion to the original
walk. Equivalence of visual measure with the compact real boundary measure
class gives the Lebesgue-chart corollary. Almost-sure convergence and uniqueness
of limits identify any other almost-sure version of the hitting map with the
named map used in the theorem.

## Inspecting the dependencies

The folder contains the complete local import closure, including lower-level
lemmas and auxiliary results housed in those modules. `SOURCE_MANIFEST.json`
lists all direct imports and source hashes. `Audit.lean` checks each included
theorem and definition, and the main theorem's own axiom report also audits
its dependencies transitively.

This guide is a navigation aid; the Lean declarations contain the precise
hypotheses and the proofs.
