# Recursive Identity Dynamics

### Experimental symbolic dynamics prototype

Recursive Identity Dynamics is a small research prototype for studying recursive symbolic update, reinforcement, competition, decay, memory pressure, and thresholded commitment in a hand-designed symbolic system.

The implementation does not attempt to model consciousness or demonstrate the spontaneous emergence of identity. Its default experiment is deliberately structured around the symbol `self`: several symbols compete under reinforcement dynamics, while a commit gate tests whether `self` becomes sufficiently strong, persistent, contextually diverse, and structurally stable to be locked as the system's designated invariant.

## What the system implements

On each iteration, the system:

1. tokenizes an input stimulus;
2. stores the resulting symbolic trace in memory;
3. builds and updates a directed typed symbol graph;
4. tracks token frequency, context, reinforcement strength, and decay;
5. infers a small set of rule-based goals from the current tokens;
6. applies recent-memory and reinforcement pressure to later interpretation;
7. computes heuristic coherence and integrity scores;
8. checks simple graph-based contradictions; and
9. evaluates a commit gate for the designated invariant `self`.

The default driver generates a stochastic stream of symbolic stimuli and records the system state across repeated updates. A final run summary is written to `summary.json`.

## Commit gate

The commit gate is a designed experimental mechanism rather than an unconstrained discovery process.

In the current implementation, `self` is the only allowable invariant. It can be locked only after satisfying explicit conditions including:

- a minimum number of turns;
- leadership over the other configured competitor symbols;
- minimum reinforcement strength;
- a minimum strength margin over the runner-up;
- minimum contextual diversity;
- sufficient integrity;
- an allowed stabilization mode; and
- persistence across consecutive evaluations.

The purpose of the experiment is to study the behaviour of this symbolic convergence and commitment mechanism under recursive reinforcement, not to claim that the system independently discovers a self-concept.

## Main components

- `mirror1.py` - main update loop, stimulus generation, state integration, and summary export
- `tokenizer.py` - lowercase word tokenization and filtering
- `interpreter.py` - token biasing, fixed symbolic definitions, simple relation extraction, and rule-based goal inference
- `memory.py` - event trace and recent symbolic pressure
- `meaning_store.py` - frequency, context, reinforcement, decay, dominance, and invariant storage
- `symbol_graph.py` - directed typed graph, implication closure, and cycle detection
- `contradiction_engine.py` - graph-based contradiction checks
- `goal_loop.py` - simple goal tracking and coherence scoring
- `self_model.py` - stabilization state, binding strength, and commit-gate logic
- `integrity.py` - bounded heuristic integrity score
- `integrity_filter.py` - rule-based intervention checks
- `observer.py` - event recording and notification of a locked invariant

## Scope and limitations

Recursive Identity Dynamics is intentionally narrow.

- The symbolic vocabulary, goal rules, scoring functions, thresholds, and commitment criteria are hand-designed.
- `self` is explicitly privileged by the current commit-gate configuration and is the only symbol that can be locked as an invariant.
- The default stimulus generator uses randomness and includes a small late-phase bias toward `self`, so the default run is not deterministic unless the random process is controlled externally.
- The meanings associated with symbols are simple stored or templated descriptions, not learned semantic representations.
- Integrity, coherence, binding, and contradiction measures are operational quantities defined by the program. They should not be interpreted as measurements of psychological or cognitive properties.
- The software makes no claim of consciousness, awareness, observerhood, general intelligence, or autonomous self-discovery.

The project is best understood as an executable symbolic experiment: a compact environment for inspecting how explicit recursive update rules can produce convergence, competition, stabilization, and thresholded commitment.

## Project history

The prototype was originally released as **Mirror-1**. The research-facing project name is now **Recursive Identity Dynamics**; the existing repository path and implementation filenames are retained for continuity with the archived release.

## Citation

The archived v1.0.0 release remains citable under its original title:

> Smith, L. C. (2026). *Mirror-1* (Version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.21131741
