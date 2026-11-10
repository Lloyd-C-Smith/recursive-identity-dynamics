# AION model specification

## Scope

The engine is an online symbolic competition model. It does not parse logical contradictions, learn meanings, infer an observer core or implement autonomous goal pursuit. The legacy RID modules are retained separately, unchanged.

## Symmetric recursive update

Let `E_t` be the set of distinct observed symbols at turn `t`, `w_s` the previous nonnegative strength of symbol `s`, and `H` the preceding bounded event window. Define:

- `p_s = w_s / sum_j w_j`, or zero when the total is zero;
- `r_s = count(events in H containing s) / len(H)`, or zero for an empty history.

The update is:

```text
w_s(next) = decay * w_s
          + observation_gain * 1[s in E_t]
          + memory_gain * r_s
          + feedback_gain * p_s^2
```

The previous state and previous window are used in this equation; the current event is appended afterwards. The squared share is explicit nonlinear positive feedback. It is designed, not learned. Every observed symbol obeys the same equation, including `self`. New symbols start with zero strength; none are pre-seeded.

Feedback can preserve residual scores during silence. A score alone is therefore never sufficient for continued commitment: recent external observations must remain in the evidence window.

History holds at most `memory_window` events. The vocabulary is capped by `max_symbols`, and per-event tokens and text size are capped. Exceeding capacity raises an error before `observe()` changes state; symbols are not silently evicted. Event duplicates are deduplicated after validating the raw token count.

## Selection and commitment

Shares are normalized strengths. A unique numerical leader must exist: shares within `1e-12` of the highest are treated as tied and remain unresolved. Lexicographic ordering is used for serialization, never to choose a winner.

The gate requires all of:

1. `min_turns` elapsed;
2. top share at least `min_share` and top-minus-runner-up at least `min_margin`;
3. at least `min_observations` events containing the candidate in the current window;
4. at least `min_contexts` distinct nonempty co-occurring symbol sets in that window;
5. the same candidate qualifying for `commit_patience` consecutive evaluations.

An empty context does not contribute diversity. Contexts are sets, not natural-language meanings. A failure or candidate change resets the qualification streak. Configurable thresholds are experimental assumptions, not derived laws.

## Continued support and release

A committed symbol must remain the unique leader, retain a share of at least `min_share * retention_ratio`, and retain at least `ceil(min_observations * retention_ratio)` recent observations plus the configured context diversity. The acquisition margin and minimum age are not re-applied during retention. Failures accumulate until `release_patience`, then the commitment is released. A supported evaluation resets the failure count. Re-acquisition starts on a subsequent event, not on the release event.

The three statuses are `UNRESOLVED`, `CANDIDATE`, and `COMMITTED`. The event stream records `committed` and `released`; it does not manufacture fission, merge, consciousness or observer-collapse diagnoses.

## Reproducibility and persistence

The update itself is deterministic for a supplied event sequence. A private `random.Random(seed)` generates synthetic inputs. Checkpoints use validated JSON, preserve RNG state, and include schema/version identifiers. They never load pickle or executable objects. Checkpoint files are atomically replaced. Output reports identify the package version, Python version, exact configuration, input hash and SHA-256 fingerprint of the engine's Python source files.

Checkpoints restore an engine, not an external experiment scheduler or file cursor. Repeat workload flags for synthetic continuation, or explicitly supply the next input events. Exact continuation is tested on one Python runtime; cross-version PRNG sampling equivalence is not assumed.

## Controls

The benchmark generates one input stream per seed/scenario and reuses it for every variant. It records every run, including non-commitments, with matching input hashes.

| Variant | Change from full model |
| --- | --- |
| `no_feedback` | Set `feedback_gain=0` |
| `no_memory` | Set `memory_gain=0`; the gate still uses recent evidence |
| `evidence_only` | Set both pressure gains to zero; retain decay and the gate |
| `no_context_gate` | Set `min_contexts=0` |
| `no_persistence` | Set `commit_patience=1`; release patience is unchanged |

Overall and recent-window modal-symbol baselines are also reported, with ties returning `None`. They have no commitment state and are not scored as if they did.

Regimes are uniformly sampled pairs (`balanced`), explicitly biased input (`dominant`), a change of biased input halfway through (`switch`), and biased input followed by empty events (`silence`). Focal symbols are sampled rather than reserved. The synthetic design labels are reported to prevent a selected input bias being mistaken for an emergent preference.

These controls measure programmed dynamics. They do not establish that feedback improves task performance or that selected labels encode identity independent of input frequency.
