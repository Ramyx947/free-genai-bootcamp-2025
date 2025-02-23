#!/usr/bin/env python3
import subprocess
import sys


def run_command(command, description):
    print(f"\n=== Running {description} ===")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ {description} failed!")
        sys.exit(result.returncode)
    print(f"✅ {description} passed!")


def main():
    # Run linting checks
    run_command("black . --check", "Black code formatting check")
    run_command("isort . --check-only", "Import sorting check")
    run_command("flake8 .", "Flake8 style check")

    # Run security checks
    run_command("bandit -r vocab_importer/", "Bandit security check")
    run_command("safety check", "Safety dependency check")

    # Run tests with coverage
    run_command(
        "pytest tests/ -v "
        "--cov=vocab_importer "
        "--cov-report=term-missing "
        "--cov-report=html",
        "Unit tests with coverage",
    )


if __name__ == "__main__":
    main()
