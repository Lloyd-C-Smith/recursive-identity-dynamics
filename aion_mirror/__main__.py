"""Command line interface: python -m aion_mirror --help."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from .core import Aion, Config, VERSION, write_json
from .experiments import VOCABULARY, benchmark, provenance


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AION | Recursive Identity Lab")
    parser.add_argument("--version", action="version", version=f"AION {VERSION}")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="run synthetic stimuli or a text file")
    run.add_argument("--steps", type=int, help="default: 200 synthetic events, or all input lines")
    run.add_argument("--seed", type=int)
    run.add_argument("--config", type=Path, help="JSON object of Config overrides")
    run.add_argument("--vocabulary", nargs="+", default=list(VOCABULARY))
    run.add_argument("--focus", help="explicitly bias synthetic input toward this symbol")
    run.add_argument("--input", type=Path, help="one stimulus per line; blank lines are silence")
    run.add_argument("--output", type=Path, default=Path("results/run.json"))
    run.add_argument("--trace", type=Path, help="stream per-turn JSONL without retaining it in memory")
    run.add_argument("--checkpoint", type=Path)
    run.add_argument("--resume", type=Path)
    bench = commands.add_parser("benchmark", help="matched-input, multi-seed ablations")
    bench.add_argument("--seeds", type=int, default=10, help="number of seeds, starting at zero")
    bench.add_argument("--steps", type=int, default=300)
    bench.add_argument("--vocabulary", nargs="+", default=list(VOCABULARY))
    bench.add_argument("--output", type=Path, default=Path("results/benchmark.json"))
    args = parser.parse_args(argv)
    try:
        if args.command == "benchmark":
            if args.seeds < 1:
                raise ValueError("--seeds must be positive")
            report = benchmark(range(args.seeds), args.steps, vocabulary=args.vocabulary)
            write_json(args.output, report)
            print(f"Wrote {len(report['trials'])} matched-input trials to {args.output}")
            return 0
        if args.steps is not None and args.steps < 1:
            raise ValueError("--steps must be positive")
        if args.resume and (args.config is not None or args.seed is not None):
            raise ValueError("--resume restores config and seed; do not also supply --config or --seed")
        if args.input and args.focus is not None:
            raise ValueError("--focus applies only to synthetic inputs")
        destinations = [p.resolve() for p in (args.output, args.trace, args.checkpoint) if p is not None]
        sources = [p.resolve() for p in (args.input, args.config, args.resume) if p is not None]
        if len(destinations) != len(set(destinations)) or set(destinations).intersection(sources):
            raise ValueError("input, output, trace and checkpoint paths must be distinct")
        if args.resume:
            engine = Aion.load(args.resume)
        else:
            config = Config(**json.loads(args.config.read_text(encoding="utf-8"))) if args.config else Config()
            engine = Aion(config, seed=args.seed if args.seed is not None else 0)
        limit = args.steps if args.steps is not None else (None if args.input else 200)
        start_turn = engine.turn
        digest = hashlib.sha256()
        with ExitStack() as stack:
            trace = None
            if args.trace:
                args.trace.parent.mkdir(parents=True, exist_ok=True)
                trace = stack.enter_context(args.trace.open("w", encoding="utf-8"))
            source = stack.enter_context(args.input.open(encoding="utf-8")) if args.input else None
            while limit is None or engine.turn - start_turn < limit:
                if source is not None:
                    text = source.readline()
                    if text == "":
                        break
                    state = engine.step(text.rstrip("\r\n"))
                    digest.update(text.encode())
                else:
                    event = engine.sample(args.vocabulary, args.focus)
                    state = engine.observe(event)
                    digest.update((json.dumps(event, ensure_ascii=False) + "\n").encode())
                if trace:
                    trace.write(json.dumps(state, sort_keys=True, allow_nan=False) + "\n")
        report = {"provenance": provenance(), "config": asdict(engine.config), "seed": engine.seed,
                  "start_turn": start_turn, "steps_executed": engine.turn - start_turn,
                  "input_sha256": digest.hexdigest(), "input_kind": "text-lines" if args.input else "synthetic-pairs",
                  "focus": args.focus, "vocabulary": args.vocabulary, "result": engine.snapshot()}
        if args.checkpoint:
            engine.save(args.checkpoint)
        write_json(args.output, report)
        print(f"AION: {engine.turn} turns | {engine.snapshot()['status']} | invariant={engine.invariant!r}")
        print(f"Summary: {args.output}")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
