"""A label-symmetric, bounded symbolic stabilization experiment.

Scores and commitment are operational measurements, not claims of observerhood.
The historical RID implementation is deliberately left unchanged.
"""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import random
import re
import tempfile
from typing import Any, Iterable

VERSION = "2.0.0.dev0"
SCHEMA = "aion-checkpoint-v1"


@dataclass(frozen=True)
class Config:
    decay: float = 0.94
    observation_gain: float = 1.0
    memory_gain: float = 0.35
    feedback_gain: float = 0.60
    memory_window: int = 32
    min_turns: int = 8
    min_observations: int = 5
    min_contexts: int = 2
    min_share: float = 0.34
    min_margin: float = 0.08
    commit_patience: int = 4
    release_patience: int = 3
    retention_ratio: float = 0.65
    max_symbols: int = 4096
    max_tokens_per_step: int = 128
    max_input_chars: int = 32768

    def __post_init__(self) -> None:
        integers = ("memory_window", "min_turns", "min_observations", "min_contexts",
                    "commit_patience", "release_patience", "max_symbols",
                    "max_tokens_per_step", "max_input_chars")
        for name in integers:
            value = getattr(self, name)
            floor = 0 if name == "min_contexts" else 1
            if type(value) is not int or value < floor:
                raise ValueError(f"{name} must be an integer >= {floor}")
        for name in ("decay", "observation_gain", "memory_gain", "feedback_gain",
                     "min_share", "min_margin", "retention_ratio"):
            value = getattr(self, name)
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if not 0 <= self.decay < 1:
            raise ValueError("decay must be in [0, 1)")
        if not 0 < self.observation_gain <= 1e6:
            raise ValueError("observation_gain must be in (0, 1e6]")
        if not all(0 <= v <= 1e6 for v in (self.memory_gain, self.feedback_gain)):
            raise ValueError("memory_gain and feedback_gain must be in [0, 1e6]")
        if not all(0 < v <= 1 for v in (self.min_share, self.min_margin, self.retention_ratio)):
            raise ValueError("share, margin and retention thresholds must be in (0, 1]")
        if max(self.min_observations, self.min_contexts) > self.memory_window:
            raise ValueError("evidence requirements cannot exceed memory_window")


def write_json(path: str | Path, data: Any) -> None:
    """Atomically replace a JSON file; never deserialize executable objects."""
    path = Path(path)
    text = json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(text)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _symbol(value: Any) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 128


class Aion:
    """Online symbolic competition with no reserved symbol and reversible commitment."""

    def __init__(self, config: Config | None = None, seed: int = 0):
        if config is not None and not isinstance(config, Config):
            raise TypeError("config must be a Config")
        if type(seed) is not int:
            raise ValueError("seed must be an integer")
        self.config = config or Config()
        self.seed = seed
        self.rng = random.Random(seed)
        self.turn = 0
        self.scores: dict[str, float] = {}
        self.memory: deque[tuple[str, ...]] = deque(maxlen=self.config.memory_window)
        self.candidate: str | None = None
        self.streak = 0
        self.invariant: str | None = None
        self.failures = 0
        self.commits = 0
        self.releases = 0
        self.first_commit_turn: int | None = None

    def _event(self, symbols: Iterable[str]) -> tuple[str, ...]:
        if isinstance(symbols, (str, bytes)):
            raise TypeError("observe expects symbols, not text; use step(text)")
        event: set[str] = set()
        for index, symbol in enumerate(symbols):
            if index >= self.config.max_tokens_per_step:
                raise ValueError("too many input tokens")
            if not _symbol(symbol):
                raise ValueError("symbols must be nonempty strings of at most 128 characters")
            event.add(symbol)
        return tuple(sorted(event))

    def _evidence(self) -> tuple[Counter, dict[str, set[tuple[str, ...]]]]:
        counts: Counter = Counter()
        contexts: dict[str, set[tuple[str, ...]]] = {}
        for event in self.memory:
            counts.update(event)
            if len(event) > 1:
                for symbol in event:
                    contexts.setdefault(symbol, set()).add(tuple(s for s in event if s != symbol))
        return counts, contexts

    def _metrics(self) -> dict[str, Any]:
        total = math.fsum(self.scores.values())
        shares = {s: v / total if total else 0.0 for s, v in sorted(self.scores.items())}
        ranked = sorted(shares.values(), reverse=True)
        top = ranked[0] if ranked else 0.0
        leaders = [s for s, p in shares.items() if top > 0 and abs(p - top) <= 1e-12]
        entropy = -math.fsum(p * math.log(p) for p in shares.values() if p > 0)
        return {"shares": shares, "leaders": leaders,
                "leader": leaders[0] if len(leaders) == 1 else None,
                "top_share": top, "margin": top - (ranked[1] if len(ranked) > 1 else 0.0),
                "normalized_entropy": entropy / math.log(len(shares)) if len(shares) > 1 else 0.0}

    def snapshot(self) -> dict[str, Any]:
        return {"turn": self.turn,
                "status": "COMMITTED" if self.invariant else ("CANDIDATE" if self.candidate else "UNRESOLVED"),
                "invariant": self.invariant, "candidate": self.candidate, "streak": self.streak,
                "release_streak": self.failures, "commits": self.commits, "releases": self.releases,
                "first_commit_turn": self.first_commit_turn, **self._metrics()}

    def step(self, text: str) -> dict[str, Any]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if len(text) > self.config.max_input_chars:
            raise ValueError("input text is too long")
        return self.observe(re.findall(r"\b\w+(?:[-']\w+)*\b", text.lower()))

    def observe(self, symbols: Iterable[str]) -> dict[str, Any]:
        """Apply one event. Repeated tokens within an event count only once."""
        event = self._event(symbols)
        if len(set(self.scores).union(event)) > self.config.max_symbols:
            raise ValueError("symbol capacity exceeded; start a new experiment or increase max_symbols")
        cfg = self.config
        previous_counts, _ = self._evidence()
        previous_total = math.fsum(self.scores.values())
        memory_size = len(self.memory)
        present = set(event)
        # All symbols use exactly the same update, including the string 'self'.
        updated = {}
        for symbol in sorted(set(self.scores).union(event)):
            old = self.scores.get(symbol, 0.0)
            share = old / previous_total if previous_total else 0.0
            recurrence = previous_counts[symbol] / memory_size if memory_size else 0.0
            updated[symbol] = (cfg.decay * old + cfg.observation_gain * (symbol in present)
                               + cfg.memory_gain * recurrence + cfg.feedback_gain * share ** 2)
        self.scores = updated
        self.memory.append(event)
        self.turn += 1
        metrics = self._metrics()
        counts, contexts = self._evidence()
        leader = metrics["leader"]
        event_record = None
        reason = "insufficient_evidence"
        if self.invariant is not None:
            symbol = self.invariant
            supported = (leader == symbol
                         and metrics["shares"][symbol] >= cfg.min_share * cfg.retention_ratio
                         and counts[symbol] >= math.ceil(cfg.min_observations * cfg.retention_ratio)
                         and len(contexts.get(symbol, ())) >= cfg.min_contexts)
            self.failures = 0 if supported else self.failures + 1
            reason = "supported" if supported else "support_weakening"
            if self.failures >= cfg.release_patience:
                event_record = {"type": "released", "symbol": symbol, "turn": self.turn}
                self.invariant = None
                self.failures = 0
                self.releases += 1
                reason = "support_lost"
        else:
            qualified = (leader is not None and self.turn >= cfg.min_turns
                         and metrics["top_share"] >= cfg.min_share
                         and metrics["margin"] >= cfg.min_margin
                         and counts[leader] >= cfg.min_observations
                         and len(contexts.get(leader, ())) >= cfg.min_contexts)
            if qualified:
                self.streak = self.streak + 1 if self.candidate == leader else 1
                self.candidate = leader
                reason = "qualifying"
                if self.streak >= cfg.commit_patience:
                    self.invariant = leader
                    self.commits += 1
                    if self.first_commit_turn is None:
                        self.first_commit_turn = self.turn
                    event_record = {"type": "committed", "symbol": leader, "turn": self.turn}
                    self.candidate, self.streak = None, 0
                    reason = "commit_gate_passed"
            else:
                self.candidate, self.streak = None, 0
                if len(metrics["leaders"]) > 1:
                    reason = "ambiguous_leader"
        return {**self.snapshot(), "reason": reason, "event": event_record}

    def sample(self, vocabulary: Iterable[str], focus: str | None = None) -> tuple[str, ...]:
        """Generate a synthetic pair; focus is an EXPLICIT experimental input bias."""
        vocabulary = tuple(vocabulary)
        self._event(vocabulary)
        if len(vocabulary) < 2 or len(set(vocabulary)) != len(vocabulary):
            raise ValueError("vocabulary must contain at least two distinct symbols")
        if focus is not None and focus not in vocabulary:
            raise ValueError("focus must be in vocabulary")
        if focus is not None and self.rng.random() < 0.85:
            return (focus, self.rng.choice([s for s in vocabulary if s != focus]))
        return tuple(self.rng.sample(vocabulary, 2))

    def to_dict(self) -> dict[str, Any]:
        fields = ("turn", "candidate", "streak", "invariant", "failures", "commits", "releases", "first_commit_turn")
        return {"schema": SCHEMA, "version": VERSION, "config": asdict(self.config), "seed": self.seed,
                "rng_state": self.rng.getstate(), "scores": dict(self.scores),
                "memory": [list(e) for e in self.memory], "state": {k: getattr(self, k) for k in fields}}

    def save(self, path: str | Path) -> None:
        write_json(path, self.to_dict())

    @classmethod
    def load(cls, path: str | Path) -> Aion:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Aion:
        """Validate a versioned JSON checkpoint before exposing an engine."""
        try:
            required = {"schema", "version", "config", "seed", "rng_state", "scores", "memory", "state"}
            if not isinstance(data, dict) or set(data) != required or data["schema"] != SCHEMA or data["version"] != VERSION:
                raise ValueError("unsupported checkpoint schema/version")
            if set(data["config"]) != set(asdict(Config())):
                raise ValueError("incomplete configuration")
            engine = cls(Config(**data["config"]), seed=data["seed"])
            scores = data["scores"]
            if not isinstance(scores, dict) or len(scores) > engine.config.max_symbols:
                raise ValueError("invalid scores")
            if any(not _symbol(k) or type(v) not in (int, float) or not math.isfinite(v) or v < 0 or v > 1e300
                   for k, v in scores.items()):
                raise ValueError("invalid score value")
            history = data["memory"]
            if not isinstance(history, list) or len(history) > engine.config.memory_window:
                raise ValueError("invalid memory")
            for event in history:
                if not isinstance(event, list) or list(engine._event(event)) != event or not set(event) <= set(scores):
                    raise ValueError("invalid memory event")
            state = data["state"]
            fields = {"turn", "candidate", "streak", "invariant", "failures", "commits", "releases", "first_commit_turn"}
            if not isinstance(state, dict) or set(state) != fields:
                raise ValueError("invalid state fields")
            for key in ("turn", "streak", "failures", "commits", "releases"):
                if type(state[key]) is not int or not 0 <= state[key] <= state["turn"]:
                    raise ValueError("invalid state counter")
            if len(history) != min(state["turn"], engine.config.memory_window):
                raise ValueError("memory length does not match turn")
            for key in ("candidate", "invariant"):
                if state[key] is not None and (not isinstance(state[key], str) or state[key] not in scores):
                    raise ValueError("unknown candidate/invariant")
            if (state["candidate"] is None) != (state["streak"] == 0) or state["streak"] >= engine.config.commit_patience:
                raise ValueError("invalid candidate streak")
            if state["invariant"] is not None and state["candidate"] is not None:
                raise ValueError("candidate and invariant cannot coexist")
            if state["failures"] >= engine.config.release_patience or (state["invariant"] is None and state["failures"]):
                raise ValueError("invalid release streak")
            if state["commits"] - state["releases"] != int(state["invariant"] is not None):
                raise ValueError("inconsistent commit/release counters")
            first = state["first_commit_turn"]
            if (first is None) != (state["commits"] == 0) or (first is not None and (type(first) is not int or not 1 <= first <= state["turn"])):
                raise ValueError("invalid first commit turn")
            if state["turn"] == 0 and scores:
                raise ValueError("nonempty initial scores")
            def tuples(value: Any) -> Any:
                return tuple(tuples(x) for x in value) if isinstance(value, (list, tuple)) else value
            engine.rng.setstate(tuples(data["rng_state"]))
            engine.scores = dict(scores)
            engine.memory.extend(tuple(event) for event in history)
            for key, value in state.items():
                setattr(engine, key, value)
            return engine
        except (KeyError, TypeError, ValueError, OverflowError, IndexError, RecursionError) as exc:
            raise ValueError(f"invalid AION checkpoint: {exc}") from exc
