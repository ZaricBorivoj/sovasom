"""Install Codex MCP token exports from .env into your zsh startup file."""

import argparse
import os
import shlex
import tempfile
from pathlib import Path

from dotenv import dotenv_values

START = "# >>> coffee-app MCP >>>"
END = "# <<< coffee-app MCP <<<"
KEYS = ("GITHUB_PAT_TOKEN", "POSTMAN_API_KEY")
PLACEHOLDERS = {"your-github-token", "your-postman-key"}


def updated_profile(content, values):
    exports = []
    for key in KEYS:
        value = values.get(key)
        if not value or value in PLACEHOLDERS or "\n" in value or "\r" in value:
            raise ValueError(f"Set {key} to a real, single-line token in the environment file.")
        exports.append(f"export {key}={shlex.quote(value)}")
    block = "\n".join([START, *exports, END, ""])
    lines = content.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == START]
    ends = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == END]
    if not starts and not ends:
        separator = "" if not content or content.endswith("\n") else "\n"
        return content + separator + block
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError("The coffee-app MCP block is malformed; repair its markers and retry.")
    return "".join(lines[: starts[0]]) + block + "".join(lines[ends[0] + 1 :])


def main():
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=repository / ".env")
    parser.add_argument(
        "--zshrc", type=Path, default=Path(os.environ.get("ZDOTDIR") or Path.home()) / ".zshrc"
    )
    args = parser.parse_args()
    try:
        config = args.env_file.expanduser().resolve()
        if not config.is_file():
            raise ValueError("Copy .env.example to .env and fill in the two MCP tokens first.")
        profile = args.zshrc.expanduser().resolve()
        original = profile.read_text() if profile.exists() else ""
        updated = updated_profile(original, dotenv_values(config, interpolate=False))
        config.chmod(0o600)
        if updated != original:
            temporary = None
            try:
                # Replace atomically with an owner-only file, preserving any .zshrc symlink.
                with tempfile.NamedTemporaryFile(
                    mode="w", dir=profile.parent, prefix=".coffee-app-", delete=False
                ) as handle:
                    temporary = Path(handle.name)
                    handle.write(updated)
                temporary.replace(profile)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            print(f"Installed MCP exports in {profile}.")
        else:
            print("MCP exports are already up to date.")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Onboarding failed: {error}\n")
    print("Open a new terminal, then launch codex from the repository.")


if __name__ == "__main__":
    main()
