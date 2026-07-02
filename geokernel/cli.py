from __future__ import annotations

import argparse
import sys
from pathlib import Path

from geokernel.io import load_config

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="geo-kernel",
        description="A command-line tool for processing data."
    )
    parser.add_argument(
        "run",
        help="Run the geo-kernel analysis from a YAML configuration file."
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the configuration file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )
    return parser


def run_command(congig_path:Path) -> int:
    try:
        config = load_config(congig_path)
        print(f"Running analysis with configuration: {config}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":    
        return run_command(args.config)
    else:
        parser.print_help()
        return 1
    

if __name__ == "__main__":
    raise SystemExit(main())