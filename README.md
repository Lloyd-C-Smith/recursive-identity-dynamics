# AION
### Recursive Identity Lab

**What persists when the inputs change?**

AION is the next experimental engine in Lloyd Christopher Smith's **Recursive Identity Dynamics (RID) / MIRROR** programme. It studies how symbolic representations compete, accumulate support, stabilize, lose support, and re-form under recursive updates.

The new name connects the project to **Aion**, the programme's substrate/interpretation motif. The software remains a finite, inspectable mathematical model, not a claim that the motif describes physical reality.

**Status: 2.0.0.dev0 — research development version, not a published release.** The original RID source remains unchanged in `recursive_identity_dynamics/`. The new engine lives in `aion_mirror/`; the repository address is unchanged.

## The substantive upgrade

| Original RID experiment | AION engine |
| --- | --- |
| Only `self` is eligible for commitment; explicit late-phase preference | Every observed symbol is eligible under the same update and gate |
| A committed symbol stays locked | Commitments can be released and replaced when recent support fails |
| Stochastic driver uses global randomness | Private seeded generator, input hashes, configuration and source fingerprints |
| One final summary | Per-turn JSONL, versioned JSON checkpoints, exact engine/RNG continuation |
| Proposed controls | Runnable matched-input ablations, frequency baselines and synthetic perturbations |
| No test suite in the inspected baseline | Standard-library tests and a Python 3.10–3.13 CI matrix |

The new core deliberately does **not** port RID's templated meanings, hand-written goals, typed-graph inference or integrity score. Those remain available in the preserved legacy code. This is a separate, more controlled experiment, not an assertion of feature parity.

## Run it

Python **3.10 or later**. The new engine and test suite have **no third-party runtime dependencies**.

```bash
# From the checked-out repository; installation is optional.
python -m aion_mirror run --seed 42 --steps 300

# Explicitly biased input, with a trajectory and checkpoint.
python -m aion_mirror run --seed 42 --steps 300 --focus mirror \
  --trace results/trajectory.jsonl --checkpoint results/state.json

# Resume the engine and generator; retain the same workload flags.
python -m aion_mirror run --resume results/state.json --steps 300 \
  --focus mirror --output results/continued.json --checkpoint results/state-next.json

# Four regimes x six variants x ten seeds = 240 trials.
python -m aion_mirror benchmark --seeds 10 --steps 300

python -m unittest discover -s tests -v
```

For an installed `aion` command, run `python -m pip install .`. This installs the new package only; the legacy scripts keep their original dependencies and execution model. This repository has not published an `aion-mirror` package to a package index.

Without `--focus`, synthetic inputs uniformly sample pairs from the supplied vocabulary; they are not guaranteed to have equal counts in a finite run. `--focus` deliberately biases the **input**, not candidate eligibility. It is a demonstration condition, not evidence of autonomous identity discovery.

## Use your own inputs

```python
from aion_mirror import Aion, Config

engine = Aion(Config(), seed=42)
for turn in range(80):
    state = engine.observe(["anchor", f"context-{turn % 4}"])
print(state["status"], state["invariant"])
engine.save("results/checkpoint.json")
```

`observe()` accepts opaque symbol strings. Duplicate tokens within one event count once. `step(text)` adds lowercase tokenization. Nothing reserves `self`, `observer`, or any other label.

For text files, use `python -m aion_mirror run --input stimuli.txt`; each line is one stimulus and a blank line is silence. All lines are processed unless `--steps` sets a limit. `--config settings.json` accepts `Config` field overrides. `python -m aion_mirror run --help` lists the options.

Checkpoint resume restores model state, evidence history, candidate/release streaks and the generator state. It does **not** restore an external file position or choose your workload: supply the remaining input lines, or repeat the same synthetic vocabulary/focus flags. A changed workload is an intervention. Reproducibility was locally checked on Python 3.13.5; bitwise equality across Python versions is not promised.

## Model and evidence

AION combines decayed evidence, recent-memory pressure and nonlinear feedback. Commitment requires a unique leader, adequate share and margin, recent observations, contextual diversity and consecutive qualifying turns. Ties remain unresolved. Release uses a lower support threshold and its own patience window.

Read [the model specification](docs/MODEL.md), [local validation results](docs/VALIDATION.md), and [the research roadmap](RESEARCH_ROADMAP.md).

The initial local validation covered **36 tests and 240 synthetic trials**. The full model changed its commitment after all ten input-switch trials and released it in all ten silence trials. Its mean switch response took **28 turns**, versus **21.1** for the evidence-only control. That is a measured stability/adaptation trade-off, **not a general performance advantage**. These observations cover the reported seeds, defaults and workloads only.

## Scientific boundaries

An `invariant` in this API means a **revocable operational commitment**, not a proven mathematical invariant. Relabelling tests check symmetry of the implementation; they do not establish semantic identity, observerhood, consciousness or general intelligence.

Removing a privileged label is necessary for studying endogenous selection, but insufficient to demonstrate it. The biased workloads' final winners agree with a recent-frequency baseline. No claim is made that AION has escaped a frequency-based explanation. The next scientific task is to distinguish structural persistence from input-frequency tracking using held-out, frequency-matched controls.

## Lineage and citation

Project author: **Lloyd Christopher Smith**. License: MIT.

The historical RID v1 software citation is retained for that historical implementation only:

> Lloyd Christopher Smith. (2026). *Recursive Identity Dynamics* (Version v1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21131741

No DOI or published release is asserted for this AION development version. When reporting experiments, identify the AION version, Git commit, configuration, seeds and source fingerprint.
