from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import ContinuityForgeError
from .evaluator import blank_evaluation
from .models import Episode
from .pipeline import generate_to_directory, plan_to_directory, write_json
from .router import ModelRouter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="continuityforge",
        description="Plan, generate, and evaluate coherent multi-shot AI animation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Validate an episode and create a storyboard")
    plan.add_argument("episode", type=Path)
    plan.add_argument("--out", type=Path, required=True)

    generate = subparsers.add_parser("generate", help="Create a generation manifest")
    generate.add_argument("episode", type=Path)
    generate.add_argument("--config", type=Path, required=True)
    generate.add_argument("--out", type=Path, required=True)
    generate.add_argument("--dry-run", action="store_true")
    generate.add_argument("--client-timeout", type=float, default=None)

    evaluate = subparsers.add_parser("evaluate", help="Create an evaluation sheet")
    evaluate.add_argument("manifest", type=Path)
    evaluate.add_argument("--out", type=Path, required=True)
    return parser


def run(args: argparse.Namespace) -> int:
    if args.command == "plan":
        episode = Episode.load(args.episode)
        shots, path = plan_to_directory(episode, args.out)
        duration = sum(shot.duration_seconds for shot in shots)
        print(f"Planned {len(shots)} shots / {duration}s -> {path}")
        return 0

    if args.command == "generate":
        episode = Episode.load(args.episode)
        router = ModelRouter.load(args.config)
        path = generate_to_directory(
            episode,
            router,
            args.out,
            dry_run=args.dry_run,
            client_timeout=args.client_timeout,
        )
        print(f"Wrote generation manifest -> {path}")
        return 0

    if args.command == "evaluate":
        with args.manifest.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        path = write_json(args.out, blank_evaluation(manifest))
        print(f"Wrote evaluation sheet -> {path}")
        return 0

    return 2


def main() -> None:
    try:
        raise SystemExit(run(build_parser().parse_args()))
    except ContinuityForgeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()

