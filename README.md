# MIRROR

### Recursive Identity and Observer Dynamics

*What makes a changing system the same system?*

**MIRROR** is a computational research project exploring the relationship between recursive interpretation, constraint and identity.

Its motivating hypothesis is that identity need not be an object hidden inside a system. It may instead consist in an organisation that persists through change—and, in more developed cases, participates in maintaining that persistence through representations of itself.

The project asks how such organisation can arise, what sustains it, and what distinguishes a stable symbolic pattern from a system whose representation of itself influences its subsequent activity.

**Central research question:** Under what conditions does self-representation help a system maintain its organisation through change?

> Identity is not an unchanging state, but an organisation sustained through change.

This is the project's working philosophical proposition, not a result presumed by its experiments.

## Project identity

**MIRROR** names the research project and its broader conceptual architecture: **Meta-Interpreter for Recursive Representation and Observer Re-binding**.

**Recursive Identity Dynamics (RID)** remains the name of the existing computational model. The original source directory, class names and repository address are retained. MIRROR gives that model a philosophical home; it does not imply that the entire conceptual architecture is already implemented.

**Aion** and **Kairon** name complementary philosophical concepts within the project, rather than separate software agents or alternative names for the whole system.

## Philosophical foundations

### Reality and interpretation

MIRROR begins with a distinction between **reality** and **a system's interpretation of reality**. It does not require the physical world to begin with an observer. Its philosophical proposal concerns how an interpreter might arise within a world that already exists, and how that interpreter becomes part of what it represents.

A representation can be coherent without being true. Internal consistency therefore matters, but cannot replace agreement with evidence or the environment.

### Recursion: the interpreter within the process

A system's previous activity can influence how it interprets later inputs. When the system also represents aspects of its own activity, those representations may enter the process that produces its next state. The interpreter is then not merely describing a process from outside: it is a component within that process.

The distinction matters. Repeating an output is not the same as using a representation of one's own activity to shape subsequent activity. MIRROR's interest is in the latter relationship, and in how it can be distinguished from simpler feedback effects.

### Aion: interpretive possibility

**Aion** names the openness of the interpretive domain: the space of possible representations and relations available to a system.

It expresses the possibility of interpreting differently, forming new relations and reorganising an existing account. It is a conceptual name for interpretive possibility, not a claim about a separately discovered physical substance.

### Kairon: constraint

**Kairon** names constraint: the conditions that limit which interpretations can remain coherent and viable.

Memory, structure, consistency and environmental feedback can each constrain interpretation. Aion and Kairon are complementary: possibility supplies alternatives; constraint limits which alternatives can be sustained. Neither, by itself, establishes that a surviving interpretation is correct.

### Identity: continuity through change

**Identity**, in this framework, concerns continuity of organisation rather than the repetition of a label. A system repeatedly producing the word `self` would not, by that fact alone, establish the kind of identity under investigation.

The deeper question is whether some organisation persists through changing states and whether self-representation contributes to that persistence. A stable label and a self-maintaining organisation are different explanatory claims.

### The Origin Loop: recursive closure

**The Origin Loop** names a proposed form of recursive closure: the interpreter includes its own participation within its account of the process.

“Origin” therefore refers to a structural relation, not necessarily a first moment in cosmic history or a first observer. The question is how an account of a process can include the activity of the system producing that account.

### Observer re-binding and co-mirroring

**Observer re-binding** names the proposed relation between an evolving self-representation and the changing process it represents. Continuity need not require an unchanged description: the description may be revised as the system changes.

**Co-mirroring** extends the inquiry to interacting systems that represent one another and their relationship. The philosophical picture is relational: an interpreter is neither outside the world nor the only perspective within it.

Here, an observer is a proposed functional perspective within a process; the word does not by itself establish conscious experience. These concepts motivate the project and are not conclusions established merely by running the software.

## The computational model

RID provides a concrete setting for studying **recursive symbolic stabilisation**: how representations acquire persistence, dominance and commitment under repeated interpretation, memory, reinforcement, competition, decay and constraint.

On each iteration, the existing model:

1. Tokenises an incoming stimulus and stores a symbolic memory trace.
2. Updates a directed, typed graph of symbol relations.
3. Tracks token frequency, context, reinforcement, competition and decay.
4. Infers simple rule-based goals and applies recent-memory pressure to interpretation.
5. Computes operational coherence and integrity scores and checks graph-based contradictions.
6. Evaluates whether the designated candidate meets the conditions for stable commitment.

The model makes these mechanisms inspectable. Its immediate computational question is narrower than the project's philosophical question: **under what configured conditions does a symbolic representation stabilise?**

### Current implementation and scope

In the present implementation, `self` is the **sole eligible invariant**. Its commitment gate requires a minimum number of turns, leadership over configured competitors, sufficient strength and margin, contextual diversity, integrity, an allowed stabilisation mode and persistence across consecutive evaluations.

The model uses hand-designed vocabulary, rules, scoring functions and thresholds. Its stimulus distribution changes over a run, and its update loop applies additional late-phase pressure favouring `self`. Symbol meanings are stored or templated descriptions rather than learned semantic representations. Coherence, integrity, binding and contradiction are program-defined operational metrics, not psychological measurements.

Consequently, a successful lock demonstrates that the configured commitment conditions were met—not that the system independently discovered an identity. The existing model does not establish consciousness, observerhood or that self-representation causally maintains a system's organisation. Observer re-binding and co-mirroring describe the broader philosophical architecture, not completed capabilities of this implementation.

This distinction keeps the philosophical question ambitious and the computational claims specific.

## Run the existing model

From the repository root, with Python 3 available:

```bash
python -m pip install PyYAML
python recursive_identity_dynamics/recursive_identity_dynamics.py
```

The default driver performs **5,000 updates**, prints periodic state information and writes (or replaces) `summary.json` in the current working directory. When launched from the repository root as above, that output is separate from the historical summary stored inside `recursive_identity_dynamics/`.

The driver reads an optional `config.yaml` from the current working directory and falls back to an empty configuration when the file is absent. Inputs are stochastic, so results can differ between runs unless randomness is controlled.

## Implementation map

All modules below are in [`recursive_identity_dynamics/`](recursive_identity_dynamics/).

| Module | Responsibility |
| --- | --- |
| `recursive_identity_dynamics.py` | Update loop, stimulus generation, integration and summary export |
| `tokenizer.py` | Lowercase tokenisation and filtering |
| `interpreter.py` | Token biasing, fixed symbolic definitions, relation extraction and rule-based goals |
| `memory.py` | Event traces and recent symbolic pressure |
| `meaning_store.py` | Frequency, context, reinforcement, decay, dominance and invariant storage |
| `symbol_graph.py` | Typed directed graph, implication closure and cycle detection |
| `contradiction_engine.py` | Graph-based contradiction checks |
| `goal_loop.py` | Goal tracking and coherence scoring |
| `self_model.py` | Stabilisation state, binding strength and commitment gate |
| `integrity.py` | Bounded operational integrity score |
| `integrity_filter.py` | Rule-based intervention checks |
| `observer.py` | Event recording and locked-invariant notifications |

## Authorship and citation

Created by **Lloyd Christopher Smith**.

The existing software citation is retained under the original RID title:

> Lloyd Christopher Smith. (2026). *Recursive Identity Dynamics* (Version v1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21131741

The MIRROR project identity does not change the title of that historical software citation.

## Licence

See [LICENSE](LICENSE).
