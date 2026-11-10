# MIRROR

### Recursive Identity and Observer Dynamics

**A computational research project on symbolic persistence, recursive self-representation and organisational continuity.**

MIRROR investigates how a system's internal representations develop through repeated interaction, how some representations become stable, and whether representations of the system itself can contribute to the persistence of its organisation.

The project connects a philosophical question about identity through change with a computational question about the mechanisms that produce stable patterns. Its existing implementation, **Recursive Identity Dynamics (RID)**, models symbolic reinforcement, memory, competition, decay and threshold-based commitment.

**Central research question:** Under what conditions does self-representation contribute causally to a system's organisational persistence?

## Project scope

**MIRROR** names the research project: **Meta-Interpreter for Recursive Representation and Observer Re-binding**. Here, observer re-binding refers to updating the correspondence between a system's self-representation and its changing state. The name describes the conceptual scope, not a claim that all of its components are implemented.

**Recursive Identity Dynamics (RID)** remains the name of the existing computational model. The original source directory, class names and repository address are retained.

The project distinguishes three levels of analysis: the philosophical interpretation of identity, the specification of computational mechanisms, and the evidence obtained from particular runs. Claims at one level do not automatically establish claims at another.

## Theoretical and philosophical foundations

### Representation and external reality

The project distinguishes a physical or simulated process from a system's internal representation of that process. A representation is evaluated by its relation to what it represents, not solely by its internal consistency.

This distinction separates **coherence** from **accuracy**. A computational score for consistency is not, by itself, a measure of correspondence with an environment. MIRROR's philosophical starting point is that interpreters are components of the systems they investigate, rather than external prerequisites for those systems to exist.

### Representational state spaces and constraints

A **representational state space** specifies the internal configurations available to a model. **Constraints** specify which configurations and transitions are permitted or favoured by its architecture, update rules, memory and inputs.

In RID, the represented information includes symbols, contextual associations, relation graphs and accumulated strengths. Reinforcement, competition, decay and gating rules constrain how this information changes. Persistence must therefore be analysed in relation to the mechanisms and input conditions that produce it, rather than attributed to a symbol merely because it survives.

### Recursive self-modelling

**Recursive self-modelling** refers here to a proposed mechanism in which a system represents aspects of its own state or activity, and those representations influence subsequent state transitions. The representation and the represented process then participate in the same causal dynamics.

This is a stronger claim than recurrence alone. A system can depend on its previous state without maintaining an informative representation of itself. Likewise, a variable named `self` does not establish that such a representation exists. The relevant questions concern what information a representation carries, how it is updated and what difference it makes to the system's behaviour.

### Identity as organisational persistence

The working philosophical hypothesis is that identity can be investigated through **continuity of organisation**, rather than treated as a fixed internal object or an unchanged symbolic label.

For this hypothesis to support empirical analysis, the relevant organisation must be specified: which relations, functional properties or update mechanisms are expected to persist, over what interval, and under which changes in input or internal state. Persistence of a label, persistence of a pattern and maintenance of a functional organisation are distinct outcomes.

The project's question is not simply whether a representation remains dominant. It is whether self-representation contributes to maintaining specified organisational properties as the system changes.

### Endogenous observation and model updating

An **endogenous observer** is used here as a functional concept: an information-registering and model-updating process that is itself part of the system being described. Its representations must account for changes in both its environment and its own activity.

The philosophical issue is how an internal model can include the participation of the process constructing it. Computationally, this requires specifying the represented variables, the update relation and the effects of that representation on subsequent behaviour. It does not follow from giving a component an observer-related name.

### Interacting systems and reciprocal modelling

The same framework can be stated for interacting systems that represent aspects of one another. In this setting, **reciprocal modelling** concerns how each system's representations and actions affect the other's state and subsequent model updates.

This extends the philosophical account from individual persistence to relational organisation. It describes part of MIRROR's theoretical scope; the current RID implementation does not establish a multi-system reciprocal-modelling capability.

### Evidence and interpretation

The central distinction is between **observing persistence** and **identifying its cause**. Evidence that self-representation contributes to persistence would require a defined organisational measure and controlled comparisons that alter the self-representational mechanism while accounting for input history, memory and reinforcement. Merely observing a stable token cannot distinguish those explanations.

This is a criterion for interpreting the research question, not a claim that the present implementation has already satisfied it. The framework treats identity and observation as explicitly defined research concepts; it does not assume that symbolic stabilisation demonstrates conscious experience.

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

Consequently, a successful lock demonstrates that the configured commitment conditions were met—not that the system independently discovered an identity. The existing model does not establish consciousness, observerhood or that self-representation causally maintains a system's organisation. Endogenous observation and reciprocal modelling belong to the broader theoretical framework, rather than demonstrated capabilities of this implementation.

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
