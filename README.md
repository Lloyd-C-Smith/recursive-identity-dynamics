# Recursive Identity Dynamics

### A computational framework for recursive symbolic stabilization and identity dynamics

**Recursive Identity Dynamics (RID)** is an executable research framework for investigating how symbolic representations acquire persistence, dominance, and stable commitment through repeated cycles of interpretation, memory, reinforcement, competition, decay, and constraint.

**Core research question:** Under what conditions can a recursively updated symbolic system maintain a stable internal representation despite competing symbols, changing inputs, and decay?

RID treats identity stabilization as a dynamical process rather than simply a static label. Its current implementation makes that process inspectable: symbols accumulate reinforcement and contextual associations, interact in a directed typed graph, and are evaluated against explicit stability and integrity conditions. A thresholded commit gate can lock a designated representation once its criteria are satisfied.

This is a **controlled model of symbolic stabilization**, not a demonstration that consciousness or an independently discovered self-concept has emerged. Its value is in making the mechanisms and their assumptions explicit, measurable, and open to falsification.

## Why investigate this?

Stable representations are central to many computational questions: how memory influences later interpretation; how one representation outcompetes alternatives; how persistent structure survives perturbation; and how constraints determine whether a state is accepted as stable.

RID brings these questions together in a compact experimental setting. It offers a platform for asking which outcomes follow from recursive feedback, which depend on chosen parameters, and which disappear when a built-in preference is removed.

The longer-term ambition is to move from **designed stabilization** toward experimentally demonstrated **endogenous selection**. That is a research objective, not a result already established.

## How RID works

On each iteration, the system:

1. Tokenizes an incoming stimulus and stores a symbolic memory trace.
2. Updates a directed, typed graph of symbol relations.
3. Tracks token frequency, context, reinforcement, competition, and decay.
4. Infers simple rule-based goals and applies recent-memory pressure to interpretation.
5. Computes operational coherence and integrity scores and checks graph-based contradictions.
6. Evaluates whether the designated candidate meets the conditions for stable commitment.

The default driver generates stochastic symbolic stimuli, records state across updates, and writes a final `summary.json`.

### Thresholded commitment

In the present experiment, `self` is the **sole eligible invariant**. Its commit gate requires a minimum number of turns, leadership over configured competitors, sufficient strength and margin, contextual diversity, integrity, an allowed stabilization mode, and persistence across consecutive evaluations.

These criteria are deliberately specified by the experimenter. The interesting observable is **whether, when, and how the configured system satisfies them**, and how that behavior changes under controlled interventions. A successful lock is not evidence of spontaneous self-discovery.

## Research directions

- **Symbolic competition:** Map conditions under which a candidate wins, loses, or oscillates.
- **Memory-dependent interpretation:** Test whether changes to history alter future trajectories.
- **Constraint-mediated selection:** Measure the contribution of integrity and persistence gates.
- **Robustness:** Test sensitivity to seeds, parameter changes, stimulus distributions, and perturbations.
- **Endogenous selection:** Generalize beyond a privileged `self` token and test whether any stable representation is selected without a predefined winner.

See [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) for hypotheses, validation gates, and proposed next experiments.

## Implementation map

- `recursive_identity_dynamics.py` — update loop, stimulus generation, integration, and summary export
- `tokenizer.py` — lowercase tokenization and filtering
- `interpreter.py` — token biasing, fixed symbolic definitions, relation extraction, and rule-based goals
- `memory.py` — event traces and recent symbolic pressure
- `meaning_store.py` — frequency, context, reinforcement, decay, dominance, and invariant storage
- `symbol_graph.py` — typed directed graph, implication closure, and cycle detection
- `contradiction_engine.py` — graph-based contradiction checks
- `goal_loop.py` — goal tracking and coherence scoring
- `self_model.py` — stabilization state, binding strength, and commit gate
- `integrity.py` — bounded operational integrity score
- `integrity_filter.py` — rule-based intervention checks
- `observer.py` — event recording and locked-invariant notifications

## Interpretation and boundaries

RID currently uses hand-designed vocabulary, rules, scoring functions, thresholds, and commitment criteria. Its default stochastic stimulus generator includes a small late-phase bias toward `self`; runs are not deterministic unless randomness is controlled. Symbol meanings are stored or templated descriptions rather than learned semantic representations. Coherence, integrity, binding, and contradiction are **program-defined operational metrics**, not psychological measurements.

Accordingly, RID does not establish consciousness, awareness, observerhood, general intelligence, or autonomous identity discovery. Those stronger interpretations would require new definitions, controls, and independent evidence. The project's scientific promise is that these boundaries can be tested and progressively tightened rather than obscured.

## Citation

> Lloyd Christopher Smith. (2026). *Recursive Identity Dynamics* (Version v1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21131741
