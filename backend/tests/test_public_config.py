import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/check-public-config.py"


def run(repository, *arguments):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=repository,
        text=True,
        capture_output=True,
    )


def test_staged_check_rejects_index_values_even_when_working_copy_is_clean(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    example = tmp_path / "terraform.tfvars.example"
    example.write_text('aws_account_id = "111122223333"\n')
    subprocess.run(["git", "add", example.name], cwd=tmp_path, check=True)
    example.write_text('aws_account_id = "REPLACE_WITH_AWS_ACCOUNT_ID"\n')
    rejected = run(tmp_path, "--staged")
    assert rejected.returncode == 1
    assert "aws_account_id" in rejected.stderr
    assert "111122223333" not in rejected.stderr + rejected.stdout
    subprocess.run(["git", "add", example.name], cwd=tmp_path, check=True)
    assert run(tmp_path, "--staged").returncode == 0


def test_public_examples_pass_without_reading_private_local_inputs(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "terraform.tfvars.example").write_text(
        'name = "REPLACE_WITH_RESOURCE_PREFIX"\ncreate_github_oidc_provider = false\n'
    )
    (tmp_path / "backend.tfbackend.example").write_text(
        'bucket = "REPLACE_WITH_STATE_BUCKET_NAME"\nregion = "eu-central-1"\nuse_lockfile = true\n'
    )
    (tmp_path / "terraform.tfvars").write_text('name = "private-local-input"\n')
    subprocess.run(["git", "add", "*.example"], cwd=tmp_path, check=True)
    accepted = run(tmp_path)
    assert accepted.returncode == 0, accepted.stderr
    assert "2 files" in accepted.stdout
    (tmp_path / "backend.tfbackend.example").write_text('bucket = "private-local-bucket"\n')
    assert run(tmp_path).returncode == 1
