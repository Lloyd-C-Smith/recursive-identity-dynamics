"""Matched-input synthetic controls. These are experiments, not evidence of cognition."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import platform
from statistics import mean
from typing import Iterable

from .core import Aion, Config, VERSION

VOCABULARY = ("self", "mirror", "loop", "origin", "observer")
SCENARIOS = ("balanced", "dominant", "switch", "silence")


def provenance() -> dict:
    digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob("*.py")):
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return {"version": VERSION, "python": platform.python_version(), "source_sha256": digest.hexdigest()}


def _winner(counts: Counter) -> str | None:
    if not counts:
        return None
    high = max(counts.values())
    leaders = [key for key, value in counts.items() if value == high]
    return leaders[0] if len(leaders) == 1 else None


def make_stream(seed: int, steps: int, scenario: str, vocabulary: Iterable[str] = VOCABULARY) -> tuple[list, dict]:
    if type(steps) is not int or steps < 2:
        raise ValueError("steps must be an integer >= 2")
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    vocabulary = tuple(vocabulary)
    sampler = Aion(seed=seed)
    # Validate before choosing; sampling uses a private RNG, never global random state.
    sampler._event(vocabulary)
    if len(vocabulary) < 3 or len(set(vocabulary)) != len(vocabulary):
        raise ValueError("experiments require at least three distinct symbols")
    first, second = sampler.rng.sample(vocabulary, 2)
    change = steps // 2
    stream = []
    for index in range(steps):
        if scenario == "silence" and index >= change:
            stream.append(())
        else:
            focus = None if scenario == "balanced" else (second if scenario == "switch" and index >= change else first)
            stream.append(sampler.sample(vocabulary, focus))
    return stream, {"initial_focus": None if scenario == "balanced" else first,
                    "later_focus": second if scenario == "switch" else None,
                    "change_after": change if scenario in ("switch", "silence") else None}


def benchmark(seeds: Iterable[int] = range(10), steps: int = 300,
              scenarios: Iterable[str] = SCENARIOS, config: Config | None = None,
              vocabulary: Iterable[str] = VOCABULARY) -> dict:
    seeds, scenarios, vocabulary = list(seeds), tuple(scenarios), tuple(vocabulary)
    if not seeds or any(type(seed) is not int for seed in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError("supply a nonempty list of distinct integer seeds")
    if not scenarios or any(s not in SCENARIOS for s in scenarios) or len(set(scenarios)) != len(scenarios):
        raise ValueError("supply distinct supported scenarios")
    cfg = config or Config()
    variants = {"full": cfg, "no_feedback": replace(cfg, feedback_gain=0),
                "no_memory": replace(cfg, memory_gain=0),
                "evidence_only": replace(cfg, feedback_gain=0, memory_gain=0),
                "no_context_gate": replace(cfg, min_contexts=0),
                "no_persistence": replace(cfg, commit_patience=1)}
    trials = []
    for scenario in scenarios:
        for seed in seeds:
            stream, design = make_stream(seed, steps, scenario, vocabulary)
            digest = hashlib.sha256(json.dumps(stream, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
            overall = _winner(Counter(s for event in stream for s in event))
            recent = _winner(Counter(s for event in stream[-cfg.memory_window:] for s in event))
            for variant, settings in variants.items():
                engine = Aion(settings, seed)
                committed_steps, response_delay = 0, None
                for event in stream:
                    state = engine.observe(event)
                    committed_steps += int(state["invariant"] is not None)
                    if (scenario == "switch" and state["turn"] > design["change_after"]
                            and state["invariant"] == design["later_focus"] and response_delay is None):
                        response_delay = state["turn"] - design["change_after"]
                trials.append({"scenario": scenario, "seed": seed, "variant": variant,
                               "input_sha256": digest, "design": design,
                               "overall_frequency_winner": overall, "recent_frequency_winner": recent,
                               "final_invariant": engine.invariant, "first_commit_turn": engine.first_commit_turn,
                               "commits": engine.commits, "releases": engine.releases,
                               "committed_fraction": committed_steps / steps,
                               "response_delay_turns": response_delay})
    aggregates = []
    for scenario in scenarios:
        for variant in variants:
            rows = [r for r in trials if r["scenario"] == scenario and r["variant"] == variant]
            delays = [r["response_delay_turns"] for r in rows if r["response_delay_turns"] is not None]
            committed = sum(r["commits"] > 0 for r in rows)
            aggregates.append({"scenario": scenario, "variant": variant, "runs": len(rows),
                               "ever_committed": committed, "never_committed": len(rows) - committed,
                               "final_committed": sum(r["final_invariant"] is not None for r in rows),
                               "mean_committed_fraction": mean(r["committed_fraction"] for r in rows),
                               "mean_releases": mean(r["releases"] for r in rows),
                               "switch_responses": len(delays),
                               "mean_response_delay": mean(delays) if delays else None})
    return {"provenance": provenance(), "steps": steps, "seeds": seeds, "vocabulary": vocabulary,
            "variants": {k: asdict(v) for k, v in variants.items()}, "trials": trials, "aggregates": aggregates,
            "limitations": ["Synthetic stimuli; focus is deliberately biased except in balanced runs.",
                            "No proof of endogenous semantic identity, observerhood or consciousness.",
                            "Ablations retain the same evidence window and commitment bookkeeping.",
                            "No-memory disables score pressure, not the gate's evidence history.",
                            "Descriptive seed outcomes only; no broad robustness claim or significance test."]}
