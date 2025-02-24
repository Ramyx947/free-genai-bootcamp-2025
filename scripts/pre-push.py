#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
from typing import List, Optional
import argparse
import logging
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PrePushError(Exception):
    """Custom error for pre-push checks"""
    pass

def check_poetry_installation() -> None:
    """Verify Poetry is installed and working"""
    if not shutil.which('poetry'):
        raise PrePushError(
            "Poetry not found. Please install it: "
            "curl -sSL https://install.python-poetry.org | python3 -"
        )
    
    try:
        subprocess.run(
            ['poetry', '--version'],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        raise PrePushError(f"Poetry installation is broken: {e.stderr.decode()}")

def validate_python_project(project_path: Path, skip_tests: bool = False) -> bool:
    """Validate a Python project with formatting and tests."""
    try:
        if not project_path.exists():
            raise PrePushError(f"Project directory not found: {project_path}")

        # Check for pyproject.toml
        if not (project_path / "pyproject.toml").exists():
            raise PrePushError(f"pyproject.toml not found in {project_path}")

        logger.info(f"Validating {project_path.name}...")

        # Install dependencies if needed
        if not (project_path / "poetry.lock").exists():
            logger.info(f"Installing dependencies for {project_path.name}...")
            subprocess.run(
                ['poetry', 'install'],
                cwd=project_path,
                check=True,
                capture_output=True
            )

        # Run checks
        checks = [
            ['poetry', 'run', 'black', '.', '--check'],
            ['poetry', 'run', 'isort', '.', '--check-only']
        ]
        
        if not skip_tests:
            checks.append(['poetry', 'run', 'pytest'])

        for check in checks:
            try:
                subprocess.run(check, cwd=project_path, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                raise PrePushError(
                    f"'{' '.join(check)}' failed:\n{e.stderr.decode()}"
                ) from e

        logger.info(f"✅ {project_path.name} validation passed")
        return True

    except Exception as e:
        raise PrePushError(f"Error in {project_path.name}: {str(e)}") from e

def main(args: Optional[List[str]] = None) -> int:
    """Main function for pre-push checks."""
    try:
        # Check Poetry installation first
        check_poetry_installation()

        # Parse arguments
        parser = argparse.ArgumentParser(description="Run pre-push checks")
        parser.add_argument(
            "--skip-tests",
            action="store_true",
            help="Skip running tests"
        )
        parsed_args = parser.parse_args(args)

        # Get repository root
        repo_root = Path(__file__).parent.parent

        # Get changed directories
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            changed_dirs = {
                path.split('/')[0] 
                for path in result.stdout.splitlines()
            }
        except subprocess.CalledProcessError:
            logger.warning("Could not get changed files, checking all projects")
            changed_dirs = set()

        # Python projects to check
        python_projects = [
            "backend-flask",
            "vocab-importer",
            "opea-comps"
        ]

        # Validate each changed project
        for project_name in python_projects:
            if not changed_dirs or project_name in changed_dirs:
                project_path = repo_root / project_name
                try:
                    validate_python_project(project_path, skip_tests=parsed_args.skip_tests)
                except PrePushError as e:
                    logger.error(f"❌ {project_name} validation failed: {str(e)}")
                    return 1

        logger.info("✅ All pre-push checks passed")
        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Pre-push checks interrupted")
        return 1
    except Exception as e:
        logger.error(f"❌ Pre-push checks failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 