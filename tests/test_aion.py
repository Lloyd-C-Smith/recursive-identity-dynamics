from dataclasses import replace
import copy
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

from aion_mirror import Aion, Config
from aion_mirror.core import write_json
from aion_mirror.experiments import benchmark, make_stream, provenance

ROOT = Path(__file__).resolve().parents[1]
FAST = Config(memory_window=8, min_turns=2, min_observations=2,
              commit_patience=2, release_patience=2, min_share=0.30, min_margin=0.05)


def feed(engine, symbol="anchor", turns=40):
    return [engine.observe((symbol, f"context-{i % 4}")) for i in range(turns)]


class EngineTests(unittest.TestCase):
    def test_arbitrary_symbol_can_commit(self):
        engine = Aion(FAST)
        feed(engine)
        self.assertEqual(engine.invariant, "anchor")

    def test_exact_ties_are_unresolved(self):
        engine = Aion(FAST)
        for _ in range(100):
            state = engine.observe(("self", "other", "third"))
        self.assertIsNone(engine.invariant)
        self.assertIsNone(state["leader"])
        self.assertEqual(state["reason"], "ambiguous_leader")

    def test_label_permutation_equivariance(self):
        mapping = {"self": "zz", "mirror": "aa", "loop": "mm", "origin": "cc", "observer": "qq"}
        left, right = Aion(FAST), Aion(FAST)
        stream, _ = make_stream(7, 150, "switch")
        for event in stream:
            a = left.observe(event)
            b = right.observe(mapping[s] for s in event)
            for field in ("invariant", "candidate", "leader"):
                self.assertEqual(mapping.get(a[field]), b[field])
            self.assertEqual(a["status"], b["status"])
            for symbol, share in a["shares"].items():
                self.assertAlmostEqual(share, b["shares"][mapping[symbol]], places=14)
        self.assertGreater(left.commits, 0)

    def test_token_order_and_duplicates_do_not_bias_scores(self):
        left, right = Aion(FAST), Aion(FAST)
        for i in range(40):
            a = left.observe(("hub", str(i % 3)))
            b = right.observe((str(i % 3), "hub", "hub"))
            self.assertEqual(a, b)

    def test_context_gate_can_block_commit(self):
        strict, relaxed = Aion(FAST), Aion(replace(FAST, min_contexts=0))
        for _ in range(30):
            strict.observe(("anchor",))
            relaxed.observe(("anchor",))
        self.assertIsNone(strict.invariant)
        self.assertEqual(relaxed.invariant, "anchor")

    def test_changed_input_releases_and_rebinds(self):
        engine = Aion(FAST)
        feed(engine, "before")
        states = feed(engine, "after", 100)
        self.assertEqual(engine.invariant, "after")
        self.assertGreaterEqual(engine.releases, 1)
        self.assertTrue(any(s["event"] and s["event"]["type"] == "released" for s in states))

    def test_silence_releases_commitment(self):
        engine = Aion(FAST)
        feed(engine)
        for _ in range(FAST.memory_window + FAST.release_patience + 5):
            engine.observe(())
        self.assertIsNone(engine.invariant)
        self.assertEqual(engine.releases, 1)

    def test_gate_requires_consecutive_support(self):
        cfg = replace(FAST, decay=0, memory_gain=0, feedback_gain=0, min_turns=1,
                      min_observations=1, min_contexts=0, commit_patience=3)
        engine = Aion(cfg)
        for symbol in ("a", "a", "b", "a", "a"):
            engine.observe((symbol,))
            self.assertIsNone(engine.invariant)
        engine.observe(("a",))
        self.assertEqual(engine.invariant, "a")

    def test_memory_is_bounded(self):
        engine = Aion(FAST)
        feed(engine, turns=200)
        self.assertEqual(len(engine.memory), FAST.memory_window)

    def test_invalid_event_does_not_mutate_state(self):
        engine = Aion(replace(FAST, max_symbols=2))
        engine.observe(("a", "b"))
        before = engine.to_dict()
        with self.assertRaises(ValueError):
            engine.observe(("c",))
        self.assertEqual(before, engine.to_dict())

    def test_input_limits(self):
        engine = Aion(replace(FAST, max_tokens_per_step=2, max_input_chars=8))
        for event in (("a", "b", "c"), ("",), (123,), ("x" * 129,)):
            with self.assertRaises(ValueError):
                engine.observe(event)
        with self.assertRaises(ValueError):
            engine.step("x" * 9)
        with self.assertRaises(TypeError):
            engine.observe("text")
        self.assertEqual(engine.turn, 0)

    def test_text_tokenization(self):
        engine = Aion(FAST)
        engine.step("SELF, self! mirror-loop")
        self.assertEqual(engine.memory[-1], ("mirror-loop", "self"))

    def test_blank_input_is_valid_silence(self):
        engine = Aion(FAST)
        state = engine.step("")
        self.assertEqual(state["turn"], 1)
        self.assertEqual(state["shares"], {})

    def test_metrics_remain_finite(self):
        engine = Aion(FAST)
        for i in range(1000):
            state = engine.observe(("hub", str(i % 4)))
            self.assertTrue(all(math.isfinite(v) and 0 <= v <= 1 for v in state["shares"].values()))
            self.assertAlmostEqual(sum(state["shares"].values()), 1.0)
            self.assertTrue(-1e-12 <= state["normalized_entropy"] <= 1 + 1e-12)

    def test_snapshot_does_not_expose_internal_scores(self):
        engine = Aion(FAST)
        engine.observe(("a",))
        view = engine.snapshot()
        view["shares"]["a"] = 999
        self.assertEqual(engine.snapshot()["shares"]["a"], 1.0)

    def test_invalid_configs(self):
        examples = ({"decay": 1}, {"decay": -1}, {"feedback_gain": float("nan")},
                    {"memory_window": True}, {"min_margin": 0}, {"retention_ratio": 2},
                    {"min_contexts": -1}, {"min_turns": 0}, {"min_observations": 100},
                    {"observation_gain": 0}, {"memory_gain": -1}, {"min_share": float("inf")})
        for change in examples:
            with self.subTest(change=change), self.assertRaises(ValueError):
                Config(**change)

    def test_local_rng_is_reproducible(self):
        left, right = Aion(seed=71), Aion(seed=71)
        for _ in range(50):
            random.random()
            self.assertEqual(left.sample(("a", "b", "c")), right.sample(("a", "b", "c")))

    def test_global_rng_is_not_modified(self):
        before = random.getstate()
        Aion(seed=5).sample(("a", "b", "c"))
        self.assertEqual(before, random.getstate())

    def test_invalid_sampler_arguments(self):
        engine = Aion()
        for vocab, focus in [(("a",), None), (("a", "a"), None), (("a", "b"), "c")]:
            with self.assertRaises(ValueError):
                engine.sample(vocab, focus)


class CheckpointTests(unittest.TestCase):
    def test_roundtrip_resumes_exact_trajectory_and_rng(self):
        engine = Aion(FAST, 17)
        feed(engine)
        engine.sample(("a", "b", "c"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            engine.save(path)
            restored = Aion.load(path)
        self.assertEqual(engine.snapshot(), restored.snapshot())
        for _ in range(30):
            a = engine.sample(("a", "b", "c"))
            b = restored.sample(("a", "b", "c"))
            self.assertEqual(a, b)
            self.assertEqual(engine.observe(a), restored.observe(b))

    def test_candidate_streak_survives_roundtrip(self):
        engine = Aion(replace(FAST, min_contexts=0, commit_patience=5))
        for _ in range(3):
            engine.observe(("a",))
        self.assertGreater(engine.streak, 0)
        restored = Aion.from_dict(json.loads(json.dumps(engine.to_dict())))
        for _ in range(5):
            self.assertEqual(engine.observe(("a",)), restored.observe(("a",)))

    def test_pending_release_survives_roundtrip(self):
        engine = Aion(FAST)
        feed(engine)
        while engine.failures == 0:
            engine.observe(())
        restored = Aion.from_dict(engine.to_dict())
        self.assertEqual(engine.observe(()), restored.observe(()))
        self.assertIsNone(restored.invariant)

    def test_rejects_corrupt_checkpoint(self):
        engine = Aion(FAST)
        feed(engine)
        original = engine.to_dict()
        changes = [("schema", "unknown"), ("version", "999"), ("rng_state", []),
                   ("memory", []), ("seed", True), ("scores", {"a": float("nan")})]
        for key, value in changes:
            corrupted = copy.deepcopy(original)
            corrupted[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                Aion.from_dict(corrupted)

    def test_rejects_inconsistent_state(self):
        original = Aion(FAST).to_dict()
        for key, value in [("turn", -1), ("invariant", "missing"), ("streak", 2),
                           ("failures", 1), ("first_commit_turn", 1), ("commits", 1)]:
            state = copy.deepcopy(original)
            state["state"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                Aion.from_dict(state)

    def test_atomic_json_rejects_nan_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            write_json(path, {"safe": True})
            with self.assertRaises(ValueError):
                write_json(path, {"bad": float("nan")})
            self.assertEqual(json.loads(path.read_text()), {"safe": True})


class ExperimentTests(unittest.TestCase):
    def test_repeated_benchmarks_match(self):
        self.assertEqual(benchmark([0, 1], 60), benchmark([0, 1], 60))

    def test_ablation_inputs_are_identical(self):
        report = benchmark([0, 1], 60)
        for seed in [0, 1]:
            for scenario in ("balanced", "dominant", "switch", "silence"):
                rows = [r for r in report["trials"] if r["seed"] == seed and r["scenario"] == scenario]
                self.assertEqual(len(rows), 6)
                self.assertEqual(len({r["input_sha256"] for r in rows}), 1)

    def test_experiment_validation(self):
        for seeds in ([], [1, 1], [True]):
            with self.assertRaises(ValueError):
                benchmark(seeds, 10)
        for steps, scenario in [(1, "balanced"), (10, "unknown")]:
            with self.assertRaises(ValueError):
                make_stream(0, steps, scenario)

    def test_held_out_vocabulary_runs(self):
        report = benchmark([0], 40, vocabulary=("red", "blue", "green"))
        self.assertEqual(len(report["trials"]), 24)
        self.assertTrue(all(r["final_invariant"] in (None, "red", "blue", "green") for r in report["trials"]))

    def test_provenance_contains_source_digest(self):
        self.assertEqual(len(provenance()["source_sha256"]), 64)


class CliTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, "-m", "aion_mirror", *map(str, args)],
                              cwd=ROOT, capture_output=True, text=True, timeout=20)

    def test_help_and_version(self):
        self.assertEqual(self.invoke("--help").returncode, 0)
        self.assertIn("AION", self.invoke("--version").stdout)

    def test_run_outputs_and_checkpoint_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            args = ["run", "--steps", 40, "--focus", "mirror", "--output", p / "a.json",
                    "--trace", p / "trace.jsonl", "--checkpoint", p / "state.json"]
            process = self.invoke(*args)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(len((p / "trace.jsonl").read_text().splitlines()), 40)
            process = self.invoke("run", "--resume", p / "state.json", "--focus", "mirror",
                                  "--steps", 40, "--output", p / "b.json")
            self.assertEqual(process.returncode, 0, process.stderr)
            process = self.invoke("run", "--steps", 80, "--focus", "mirror", "--output", p / "full.json")
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads((p / "b.json").read_text())["result"],
                             json.loads((p / "full.json").read_text())["result"])

    def test_text_input_reads_all_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            (p / "inputs.txt").write_text("alpha beta\n\nalpha gamma\n", encoding="utf-8")
            process = self.invoke("run", "--input", p / "inputs.txt", "--output", p / "out.json")
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads((p / "out.json").read_text())["steps_executed"], 3)

    def test_invalid_cli_fails_without_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "out.json"
            process = self.invoke("run", "--steps", 0, "--output", p)
            self.assertNotEqual(process.returncode, 0)
            self.assertFalse(p.exists())

    def test_cli_refuses_path_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "out.json"
            process = self.invoke("run", "--output", p, "--checkpoint", p)
            self.assertNotEqual(process.returncode, 0)
            self.assertFalse(p.exists())

    def test_benchmark_command(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "bench.json"
            process = self.invoke("benchmark", "--seeds", 1, "--steps", 40, "--output", p)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(len(json.loads(p.read_text())["trials"]), 24)


if __name__ == "__main__":
    unittest.main()
