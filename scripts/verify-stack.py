"""Run isolated, synthetic full-stack checks and always remove this test stack's volumes."""

import json
import os
import socket
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def main():
    with tempfile.TemporaryDirectory(prefix="office-tests-") as directory:
        root = Path(directory)
        root.chmod(0o700)
        for name, value in {
            "database_password": "synthetic-tests-only",
            "database_url": "postgresql+psycopg://office:synthetic-tests-only@db/office",
            "bootstrap.json": json.dumps(
                {
                    "email": "colleague@example.com",
                    "display_name": "Test colleague",
                    "password": "synthetic password only",
                }
            ),
        }.items():
            (root / name).write_text(value)
            # Compose file secrets must be readable by the non-root backend UID.
            # The private parent directory restricts host access.
            (root / name).chmod(0o444 if name != "bootstrap.json" else 0o600)
        https_port = free_port()
        env = {
            **os.environ,
            "COMPOSE_PROJECT_NAME": "office-test-" + uuid.uuid4().hex[:12],
            "OFFICE_SECRETS_DIR": directory,
            "SITE_ADDRESS": "localhost",
            "PUBLIC_ORIGIN": f"https://localhost:{https_port}",
            "HTTP_PORT": str(free_port()),
            "HTTPS_PORT": str(https_port),
            "E2E_BASE_URL": f"https://localhost:{https_port}",
            "OFFICE_TEST_STACK": "1",
        }

        def run(*args, **kwargs):
            return subprocess.run(args, env=env, check=True, **kwargs)

        try:
            run(
                sys.executable, "scripts/setup.py", "--bootstrap-file", str(root / "bootstrap.json")
            )
            assert not (root / "bootstrap.json").exists()
            # Rerun with different inputs; browser login below proves original credentials survive.
            (root / "bootstrap.json").write_text(
                json.dumps(
                    {
                        "email": "changed@example.com",
                        "display_name": "Changed",
                        "password": "changed synthetic password",
                    }
                )
            )
            run(
                "docker",
                "compose",
                "run",
                "--rm",
                "-T",
                "backend",
                "uv",
                "run",
                "--frozen",
                "--no-dev",
                "python",
                "-m",
                "office.setup",
                "--stdin",
                input=(root / "bootstrap.json").read_bytes(),
            )
            (root / "bootstrap.json").unlink()
            run("docker", "compose", "--profile", "test", "run", "--build", "--rm", "backend-tests")
            run("npm", "run", "test:e2e", "--", "--grep-invert", "service restart", cwd="frontend")
            env["PERSISTED_SESSION_FILE"] = str(root / "browser-session")
            env["PERSISTENCE_PHASE"] = "save"
            run("npm", "run", "test:e2e", "--", "--grep", "service restart", cwd="frontend")
            # Persisted database/session storage must survive application and DB restart.
            run("docker", "compose", "restart", "db", "backend")
            run("docker", "compose", "up", "-d", "--wait", "backend", "web")
            env["PERSISTENCE_PHASE"] = "restore"
            run("npm", "run", "test:e2e", "--", "--grep", "service restart", cwd="frontend")
        finally:
            subprocess.run(
                ["docker", "compose", "--profile", "test", "down", "--volumes", "--remove-orphans"],
                env=env,
                check=False,
            )


if __name__ == "__main__":
    main()
