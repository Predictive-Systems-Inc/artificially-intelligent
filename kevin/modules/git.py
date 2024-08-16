import subprocess
from typing import List
import click
from modules.llm import send_message
from config import config


def commit_code(history: List[str] = []) -> None:
    """
    Adds files and commits the code in the project directory to GitHub.
    """
    try:
        working_dir = config.get("dir")
        if len(history) == 0:
            click.echo("No changes to commit.")
            return False

        merged_history = " ".join(history)
        # build the commit message
        commit_message = send_message("commit_message",
                                     {"history":merged_history})
        commit_message = "Fixing lint errors"
        result = subprocess.run(["git", "add", "."], cwd=working_dir,
                                stdout=subprocess.PIPE, text=True)
        print(result.stdout)

        result = subprocess.run(["git", "commit", "-m", commit_message.strip().lower()],
                                cwd=working_dir, stdout=subprocess.PIPE, text=True)
        print(result.stdout)

        click.echo(f"Commit message: {commit_message.strip().lower()}")
        return True

    except subprocess.CalledProcessError as e:
        print("An error occurred while running lint check:")
        print("Exit Code:", e.returncode)
        print("Standard Error Output:", e.stderr)
        print("Standard Output:", e.stdout)
        return False
