# Research roadmap — AION / Recursive Identity Dynamics

## Objective

Study stability and selection under recursive symbolic updates while separating designed behavior from evidence that survives controls. AION is a new controlled engine; the historical RID implementation remains unchanged.

## Gate status in the development version

| Gate | Implemented support | Still required |
| --- | --- | --- |
| G1: Reproducibility | Local seeded RNG, input hashes, config/source provenance, checkpoint continuation tests | Independent replication and cross-platform characterization |
| G2: Baselines | Matched-input pressure ablations; overall/recent frequency baselines | Frequency-matched structural tasks and predictive baselines |
| G3: Bias audit | No privileged candidate name; label-permutation tests; explicit input-bias metadata | Wider vocabulary, initialization and parameter sweeps |
| G4: Robustness | Switch/silence scenarios; recorded multi-seed outcomes | Broad sweeps, uncertainty estimates and adversarial perturbations |
| G5: Ablations | Feedback, memory pressure, context gate and acquisition-patience controls | Separate integrity/coherence controls require a justified future model |
| G6: Unprivileged candidates | All observed symbols use symmetric rules; ties unresolved | Show persistence not explained by frequency; not yet established |
| G7: Generalization | Arbitrary symbol API and held-out-vocabulary smoke test | Meaningful held-out tasks, not merely renamed tokens |

Implemented support is **not** the same as passing a scientific validation gate. The initial observations are documented in `docs/VALIDATION.md`.

## Hypotheses to test next

**H1 — Feedback contribution.** On fixed-frequency, matched-exposure tasks, recursive feedback changes persistence in a way not reproduced by decayed counts alone. Failure: the full model is indistinguishable from a simple baseline or only adds lag.

**H2 — Constraint contribution.** Context and persistence gates reduce transient commitments without unacceptable adaptation costs. Failure: they merely delay both desirable and undesirable commitments, with no useful discrimination.

**H3 — Robustness.** Effects survive seeds, parameter neighborhoods and held-out stimulus regimes. Failure: results depend on a narrow tuning choice.

**H4 — Structural selection.** A future relation-aware model selects stable structures when token counts are matched. Failure: the apparent invariant is only the most frequent token. AION's present token-strength model does not establish H4.

## Next architectural steps

Define structural equivalence before adding a multi-symbol core detector. Preserve provenance under relabelling and changing representations; explicitly represent unresolved cases. Add relational or predictive measurements only with null models and independent falsification tests. Derive any future recursive self-reliability mechanism mathematically before calling it observerhood.

Do not infer consciousness, ontology, physical laws or general intelligence from a threshold crossing. The programme can retain ambitious questions while making each computational claim narrower and testable.

## Reporting standard

Report source revision, configuration, all seeds, input regime/hash, every winner and non-winner, commit/release times, persistence, and ablation condition. Separate observations, mechanisms and speculative implications. Publish failures and null results alongside positive examples. No new software DOI is claimed for this development version.
