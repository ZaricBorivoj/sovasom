import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/configure-corporate-ca.sh"
KEYS = (
    "AWS_CA_BUNDLE",
    "SSL_CERT_FILE",
    "CURL_CA_BUNDLE",
    "REQUESTS_CA_BUNDLE",
    "NODE_EXTRA_CA_CERTS",
)


def configure(bundle, profile, **kwargs):
    return subprocess.run(
        ["bash", str(SCRIPT), str(bundle), str(profile)],
        capture_output=True,
        text=True,
        **kwargs,
    )


def test_settings_survive_a_new_shell_and_reruns_preserve_dotfile_symlink(tmp_path):
    bundle = tmp_path / "corp ' $HOME $(false) ca.pem"
    bundle.write_text("-----BEGIN CERTIFICATE-----\nsynthetic\n-----END CERTIFICATE-----\n")
    target = tmp_path / "dotfile"
    target.write_text("export KEEP_ME=preserved\nexport AWS_CA_BUNDLE=old\n")
    target.chmod(0o600)
    profile = tmp_path / ".zshrc"
    profile.symlink_to(target)
    result = configure(bundle, profile)
    assert result.returncode == 0, result.stderr
    original = target.read_text()
    assert configure(bundle, profile).returncode == 0
    assert target.read_text() == original
    assert profile.is_symlink()
    assert target.stat().st_mode & 0o777 == 0o600
    for shell in filter(None, [shutil.which("bash"), shutil.which("zsh")]):
        result = subprocess.run(
            [
                shell,
                "-f",
                "-c",
                'source "$1"; "$2" -c "$3"',
                "check",
                str(profile),
                sys.executable,
                "import os,json; print(json.dumps({k:os.environ[k] for k in "
                f"{[*KEYS, 'KEEP_ME']!r}" + "}))",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        assert json.loads(result.stdout) == {
            **dict.fromkeys(KEYS, str(bundle)),
            "KEEP_ME": "preserved",
        }


@pytest.mark.parametrize("content", ["", "not a certificate", None])
def test_invalid_bundle_preserves_existing_shell_configuration(tmp_path, content):
    bundle = tmp_path / "ca.pem"
    if content is not None:
        bundle.write_text(content)
    profile = tmp_path / ".zshrc"
    profile.write_text("# keep this\n")
    assert configure(bundle, profile).returncode == 1
    assert profile.read_text() == "# keep this\n"


def test_malformed_managed_block_preserves_existing_shell_configuration(tmp_path):
    bundle = tmp_path / "ca.pem"
    bundle.write_text("-----BEGIN CERTIFICATE-----\nsynthetic\n-----END CERTIFICATE-----\n")
    profile = tmp_path / ".zshrc"
    original = "# >>> sovasom corporate CA >>>\n# unfinished\n"
    profile.write_text(original)
    assert configure(bundle, profile).returncode == 1
    assert profile.read_text() == original


def test_default_profile_respects_zdotdir(tmp_path):
    bundle = tmp_path / "ca.pem"
    bundle.write_text("-----BEGIN CERTIFICATE-----\nsynthetic\n-----END CERTIFICATE-----\n")
    directory = tmp_path / "zsh"
    result = subprocess.run(
        ["bash", str(SCRIPT), str(bundle)],
        env={**os.environ, "ZDOTDIR": str(directory)},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "export AWS_CA_BUNDLE=" in (directory / ".zshrc").read_text()
