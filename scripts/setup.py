"""Prepare the Compose installation from runtime input; erase the consumed file on success."""

import argparse
import json
import os
import subprocess
from pathlib import Path


def compose(*args, **kwargs):
    subprocess.run(["docker", "compose", *args], check=True, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap-file", type=Path)
    args = parser.parse_args()
    if args.bootstrap_file:
        payload = args.bootstrap_file.read_bytes()
    else:
        payload = json.dumps(
            {
                "email": os.environ.pop("INITIAL_EMAIL", ""),
                "display_name": os.environ.pop("INITIAL_DISPLAY_NAME", ""),
                "password": os.environ.pop("INITIAL_PASSWORD", ""),
            }
        ).encode()
    compose("build", "backend", "web")
    compose("up", "-d", "--wait", "db")
    compose(
        "run",
        "--rm",
        "-T",
        "--no-deps",
        "backend",
        "uv",
        "run",
        "--frozen",
        "--no-dev",
        "python",
        "-m",
        "office.setup",
        "--stdin",
        input=payload,
    )
    if args.bootstrap_file:
        args.bootstrap_file.unlink()
    compose("up", "-d", "--wait", "backend", "web")


if __name__ == "__main__":
    main()
