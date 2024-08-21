import subprocess
import os
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


def get_commit_hash_and_check_dirty(file_path) -> str:
    repo_path = Path(file_path).parent

    try:
        # Ensure the file path is relative to the repository
        relative_file_path = os.path.relpath(file_path, repo_path)

        # Get the latest commit hash for the file
        commit_hash = (
            subprocess.check_output(
                [
                    "git",
                    "-C",
                    repo_path,
                    "log",
                    "-n",
                    "1",
                    "--pretty=format:%H",
                    #"--",
                    #relative_file_path,
                ],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )

        # Check if the file is dirty (has uncommitted changes)
        diff_output = (
            subprocess.check_output(
                ["git", "-C", repo_path, "diff"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )

        # If diff_output is not empty, the file has uncommitted changes
        is_dirty = len(diff_output) > 0

        if is_dirty:
            logger.warning(f"Warning: The file {file_path} is dirty compared to the last commit. {commit_hash}")
            return 'unknown'
        if commit_hash == "":
            logger.warning(f"Warning: The file {file_path} is not under version control.")
            return 'unknown'

        print(f"Commit hash: {commit_hash}")
        return commit_hash
    except subprocess.CalledProcessError as e:
        logger.warning(f"Error: {e.output.decode('utf-8')}")
        return 'unknown'
