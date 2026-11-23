import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from dotenv import set_key

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/onboard.py"


def onboard(config, profile, **kwargs):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--env-file", str(config), "--zshrc", str(profile)],
        capture_output=True,
        text=True,
        **kwargs,
    )


def test_onboarding_preserves_shell_settings_and_safely_exports_literal_tokens(tmp_path):
    config = tmp_path / ".env"
    profile = tmp_path / ".zshrc"
    sentinel = tmp_path / "must-not-exist"
    tokens = {
        "GITHUB_PAT_TOKEN": f"synthetic' $(touch {sentinel}) `$HOME` # ${{UNCHANGED}}",
        "POSTMAN_API_KEY": 'synthetic "postman"; echo bad',
    }
    for key, value in {**tokens, "DATABASE_PASSWORD": "not-for-shell"}.items():
        set_key(config, key, value)
    original = "# Keep my settings\nexport EXISTING_SETTING=preserved"
    profile.write_text(original)
    first = onboard(config, profile)
    assert first.returncode == 0, first.stderr
    installed = profile.read_text()
    assert installed.startswith(original + "\n")
    assert "DATABASE_PASSWORD" not in installed
    assert profile.stat().st_mode & 0o777 == 0o600
    assert config.stat().st_mode & 0o777 == 0o600
    assert all(value not in first.stdout + first.stderr for value in tokens.values())
    second = onboard(config, profile)
    assert second.returncode == 0, second.stderr
    assert profile.read_text() == installed

    shell = shutil.which("zsh") or shutil.which("bash")
    assert shell, "A shell is required to verify literal token exports"
    result = subprocess.run(
        [
            shell,
            "-f",
            "-c",
            'source "$1"; exec "$2" -c "$3"',
            "check",
            str(profile),
            sys.executable,
            "import json, os; print(json.dumps({k: os.environ[k] for k in "
            '["GITHUB_PAT_TOKEN", "POSTMAN_API_KEY", "EXISTING_SETTING"]}))',
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout) == {**tokens, "EXISTING_SETTING": "preserved"}
    assert not sentinel.exists()
    set_key(config, "POSTMAN_API_KEY", "rotated-synthetic-token")
    assert onboard(config, profile).returncode == 0
    assert profile.read_text().count("export POSTMAN_API_KEY=") == 1
    assert tokens["POSTMAN_API_KEY"] not in profile.read_text()
    assert "rotated-synthetic-token" in profile.read_text()


@pytest.mark.parametrize("invalid", [None, "", "your-postman-key", "line\nbreak"])
def test_invalid_tokens_leave_profile_untouched(tmp_path, invalid):
    config = tmp_path / ".env"
    profile = tmp_path / ".zshrc"
    set_key(config, "GITHUB_PAT_TOKEN", "synthetic-github")
    if invalid is not None:
        set_key(config, "POSTMAN_API_KEY", invalid)
    profile.write_text("# unchanged\n")
    result = onboard(config, profile)
    assert result.returncode == 1
    assert "POSTMAN_API_KEY" in result.stderr
    assert "synthetic-github" not in result.stdout + result.stderr
    assert profile.read_text() == "# unchanged\n"


def test_onboarding_respects_zdotdir_and_preserves_symlink(tmp_path):
    config = tmp_path / ".env"
    for key in ("GITHUB_PAT_TOKEN", "POSTMAN_API_KEY"):
        set_key(config, key, "synthetic-token")
    dotdir = tmp_path / "zsh"
    dotdir.mkdir()
    profile = dotdir / ".zshrc"
    command = [sys.executable, str(SCRIPT), "--env-file", str(config)]
    environment = {**os.environ, "ZDOTDIR": str(dotdir)}
    result = subprocess.run(command, env=environment, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    target = tmp_path / "dotfile"
    profile.rename(target)
    profile.symlink_to(target)
    set_key(config, "POSTMAN_API_KEY", "updated-synthetic-token")
    result = subprocess.run(command, env=environment, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert profile.is_symlink()
    assert "updated-synthetic-token" in target.read_text()


@pytest.mark.parametrize(
    "content",
    [
        "# >>> coffee-app MCP >>>\n",
        "# <<< coffee-app MCP <<<\n# >>> coffee-app MCP >>>\n",
        "# >>> coffee-app MCP >>>\n# >>> coffee-app MCP >>>\n# <<< coffee-app MCP <<<\n",
    ],
)
def test_malformed_managed_blocks_are_not_overwritten(tmp_path, content):
    config = tmp_path / ".env"
    profile = tmp_path / ".zshrc"
    for key in ("GITHUB_PAT_TOKEN", "POSTMAN_API_KEY"):
        set_key(config, key, "synthetic-token")
    profile.write_text(content)
    result = onboard(config, profile)
    assert result.returncode == 1
    assert "malformed" in result.stderr
    assert profile.read_text() == content


def test_missing_env_file_does_not_create_profile(tmp_path):
    profile = tmp_path / ".zshrc"
    result = onboard(tmp_path / "missing", profile)
    assert result.returncode == 1
    assert not profile.exists()
