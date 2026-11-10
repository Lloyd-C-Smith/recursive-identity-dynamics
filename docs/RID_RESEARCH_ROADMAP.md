# Research Roadmap — Recursive Identity Dynamics

## Objective

Develop RID from a controlled symbolic commitment experiment into a rigorous testbed for **stability and selection under recursive symbolic updates**. Distinguish behavior built into the rules from behavior that emerges robustly across configurations.

This document proposes future experiments; it does not report completed empirical results.

## Research hypotheses

**H1 — Feedback sensitivity.** With stimulus distributions held fixed, changing memory/reinforcement feedback changes the distribution of dominance trajectories and commit times.

**H2 — Constraint dependence.** Integrity, diversity, and persistence requirements materially change false or transient commitment rates relative to simplified gates.

**H3 — Robust stabilization.** Some stable states persist across multiple random seeds and moderate perturbations rather than relying on a single favorable stochastic run.

**H4 — Endogenous selection (future implementation).** When multiple symbols are eligible and no candidate receives special treatment, the system can select a persistent invariant in a way that is not trivially determined by initialization or stimulus frequency.

Each hypothesis can fail; failure should be documented, not reframed as success.

## Validation gates

| Gate | Experiment | Evidence needed | Failure signal |
| --- | --- | --- | --- |
| G1: Reproducibility | Fix and record random seeds, configurations, and output summaries | Repeatable trajectories for identical inputs | Unexplained run-to-run divergence |
| G2: Baselines | Compare full model with no memory pressure, no reinforcement, and simplified gates | Measured differences from simple baselines | No meaningful difference |
| G3: Bias audit | Remove or vary late-phase `self` bias | Sensitivity curves for commit probability and timing | Outcome explained almost entirely by bias |
| G4: Robustness | Sweep parameters, seeds, competitor counts, and stimulus mixes | Distributions with uncertainty estimates | Fragility under small changes |
| G5: Ablation | Disable coherence, integrity, diversity, and persistence criteria separately | Quantified contribution of each criterion | Criteria provide no discriminating value |
| G6: Unprivileged candidates | Permit multiple invariant candidates under symmetric rules | Stable selection without a hard-coded winner | Selection vanishes or simply mirrors input frequency |
| G7: Generalization | Evaluate new symbol vocabularies and held-out stimulus regimes | Persistence of effects outside tuned examples | Effects limited to original configuration |

## Suggested experimental reporting

For every experiment record: commit SHA, configuration, seed, stimulus regime, number of runs, candidate strengths over time, winner (if any), commit timing, lock persistence, contradiction counts, and ablation condition.

Report both successes and failures, including non-commit runs. Prefer distributions across repeated trials over illustrative single trajectories. Separate **observations**, **mechanistic interpretations**, and **speculative implications**.

## Conceptual progression

1. **Designed commitment (current):** Examine how an explicitly eligible `self` representation satisfies or fails a configured gate.
2. **Competitive stabilization:** Characterize trajectories, perturbation response, and parameter regimes.
3. **Symmetric candidate selection:** Remove candidate privilege and test endogenous winner selection.
4. **Operational invariance:** Define stability under specified transformations, not just persistence across turns.
5. **Broader recursive interpretation:** Investigate coupled state/interpreter updates, with the interpreter represented within the modeled state, if a mathematically precise implementation can be specified.

The final stage is a theoretical ambition; the current software does not implement or validate it.

## Standard of evidence

A threshold crossing is a fact about a programmed threshold. A convincing scientific claim requires comparison against null models, ablations, and alternative explanations. Claims about consciousness, physics, or ontology are outside the evidence supplied by the current implementation.
