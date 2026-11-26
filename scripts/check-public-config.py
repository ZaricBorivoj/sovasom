"""Reject deployment-specific values in public Terraform example inputs."""

import argparse
import re
import subprocess
from pathlib import Path


def git(*arguments):
    return subprocess.check_output(["git", *arguments], text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staged", action="store_true", help="Check staged blobs, not working files"
    )
    args = parser.parse_args()
    if args.staged:
        paths = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0")
    else:
        paths = git("ls-files", "-z").split("\0")
    failures = []
    checked = 0
    for filename in paths:
        if not filename.endswith((".tfvars.example", ".tfbackend.example")):
            continue
        checked += 1
        content = git("show", f":{filename}") if args.staged else Path(filename).read_text()
        for number, line in enumerate(content.splitlines(), 1):
            match = re.match(r"^\s*(\w+)\s*=\s*(.*?)\s*(?:#.*)?$", line)
            if not match:
                if line.strip() and not line.lstrip().startswith("#"):
                    failures.append(f"{filename}:{number}: use simple placeholder assignments")
                continue
            key, value = match.groups()
            needs_placeholder = filename.endswith(".tfvars.example") or key not in {
                "key",
                "region",
                "encrypt",
                "use_lockfile",
                "workspace_key_prefix",
            }
            if (
                needs_placeholder
                and value not in {"true", "false"}
                and not re.fullmatch(r'"REPLACE_WITH_[A-Z0-9_]+"', value)
            ):
                failures.append(f"{filename}:{number}: {key} must use a REPLACE_WITH_* placeholder")
    if failures:
        parser.exit(1, "\n".join(failures) + "\nActual values belong in ignored local files.\n")
    print(f"Public Terraform examples passed ({checked} files).")


if __name__ == "__main__":
    main()
