"""Exercise real Terraform destroy plans on synthetic local state, without AWS access."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def check(terraform: str, root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="sovasom-terraform-test-") as temporary:
        directory = Path(temporary)
        for source in root.glob("*.tf"):
            if source.name != "backend.tf":
                shutil.copy2(source, directory / source.name)
        shutil.copy2(root / ".terraform.lock.hcl", directory)
        # These overrides exist only in this disposable copy. Never alter the
        # real provider/account checks or read an operator's backend/state.
        (directory / "test_override.tf").write_text("""
terraform {
  backend "local" {}
}
provider "aws" {
  allowed_account_ids         = null
  skip_credentials_validation = true
  skip_requesting_account_id   = true
  skip_metadata_api_check      = true
}
""")
        variables = {
            "aws_account_id": "123456789012",
            "hosted_zone_id": "Z0123456789TEST",
            "app_hostname": "coffee.example.com",
        }
        if root.name == "foundation":
            variables.update(
                name="coffee-disposable-test",
                github_oidc_subject="repo:example-org/office-ordering:ref:refs/heads/main",
                create_github_oidc_provider=True,
            )
            resources = [
                {
                    "mode": "managed",
                    "type": "aws_s3_bucket",
                    "name": "retained",
                    "provider": 'provider["registry.terraform.io/hashicorp/aws"]',
                    "instances": [
                        {
                            "index_key": purpose,
                            "schema_version": 0,
                            "attributes": {
                                "id": f"synthetic-{purpose}",
                                "bucket": f"synthetic-{purpose}",
                                "arn": f"arn:aws:s3:::synthetic-{purpose}",
                                "region": "eu-central-1",
                                "force_destroy": False,
                            },
                        }
                        for purpose in ["state", "backups"]
                    ],
                }
            ]
        else:
            variables.update(backup_bucket_name="synthetic-backups", public_ipv4="192.0.2.10")
            resources = [
                {
                    "mode": "managed",
                    "type": "aws_route53_record",
                    "name": "application",
                    "provider": 'provider["registry.terraform.io/hashicorp/aws"]',
                    "instances": [
                        {
                            "schema_version": 2,
                            "attributes": {
                                "id": "Z0123456789TEST_coffee.example.com_A",
                                "zone_id": "Z0123456789TEST",
                                "name": "coffee.example.com",
                                "type": "A",
                                "ttl": 300,
                                "records": ["192.0.2.10"],
                            },
                        }
                    ],
                }
            ]
        (directory / "terraform.tfvars.json").write_text(json.dumps(variables))
        (directory / "terraform.tfstate").write_text(
            json.dumps({"version": 4, "serial": 1, "lineage": "synthetic", "resources": resources})
        )
        environment = {
            key: value for key, value in os.environ.items() if not key.startswith(("AWS_", "TF_"))
        }
        environment.update(
            AWS_ACCESS_KEY_ID="synthetic",
            AWS_SECRET_ACCESS_KEY="synthetic",
            AWS_EC2_METADATA_DISABLED="true",
            AWS_CONFIG_FILE=str(directory / "no-config"),
            AWS_SHARED_CREDENTIALS_FILE=str(directory / "no-credentials"),
            TF_IN_AUTOMATION="true",
        )

        def run(*arguments: str) -> subprocess.CompletedProcess:
            return subprocess.run(
                [terraform, *arguments],
                cwd=directory,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

        initialized = run(
            "init",
            "-input=false",
            "-lockfile=readonly",
            "-no-color",
            f"-plugin-dir={root / '.terraform/providers'}",
        )
        if initialized.returncode:
            raise RuntimeError(initialized.stdout + initialized.stderr)
        planned = run(
            "plan", "-destroy", "-refresh=false", "-input=false", "-no-color", "-out=test.tfplan"
        )
        if root.name == "foundation":
            diagnostics = planned.stdout + planned.stderr
            if planned.returncode == 0 or "prevent_destroy" not in diagnostics:
                raise RuntimeError("Foundation destroy was not rejected:\n" + diagnostics)
            for purpose in ["state", "backups"]:
                if f'aws_s3_bucket.retained["{purpose}"]' not in diagnostics:
                    raise RuntimeError(f"Missing destroy protection for {purpose}:\n{diagnostics}")
            print("PASS: foundation destroy plan rejected for both retained buckets")
        else:
            if planned.returncode:
                raise RuntimeError(planned.stdout + planned.stderr)
            shown = run("show", "-json", "test.tfplan")
            if shown.returncode:
                raise RuntimeError(shown.stderr)
            deleted = [
                change["address"]
                for change in json.loads(shown.stdout)["resource_changes"]
                if "delete" in change["change"]["actions"]
            ]
            if deleted != ["aws_route53_record.application"]:
                raise RuntimeError(f"Unexpected application teardown ownership: {deleted}")
            print("PASS: application destroy plan deletes only its DNS record")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terraform", default="terraform")
    parser.add_argument("--root", choices=["foundation", "application"], required=True)
    args = parser.parse_args()
    check(
        shutil.which(args.terraform) or args.terraform, Path(__file__).resolve().parent / args.root
    )
