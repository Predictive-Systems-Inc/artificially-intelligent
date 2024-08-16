import subprocess
from typing import Any, Dict, List
import os

import click

from modules.llm import send_message
from modules.utils import extract_code, extract_messages, write_code_to_file
from config import config
import logging
logger = logging.getLogger(__name__)

def execute_lint() -> str:
    """
    Runs the lint command on the specified file 
    and returns the lint output.
    """
    try:
      command = config.get("lint_command").split()
      working_dir = config.get("dir")
      print(f"Running lint command: {command}")
      print(f"Working directory: {working_dir}")

      lint_result = subprocess.run(
          command,
          cwd=working_dir,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
          text=True,
      )
      return lint_result.stdout
    except subprocess.CalledProcessError as e:
        print("An error occurred while running lint check:")
        print("Exit Code:", e.returncode)
        print("Standard Error Output:", e.stderr)
        print("Standard Output:", e.stdout)
        return "" 

def read_lint_output(output: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parses the lint output and returns a list of filenames with the lint messages.
    """
    lint_messages = {}
    file_path = ""

    for line in output.splitlines():
        if "error" in line.lower():
            lint_messages[file_path].append(line)
        elif "warning" in line.lower():
            lint_messages[file_path].append(line)
        else:
            file_path = line
            lint_messages[file_path] = []
    # remove all empty lists
    lint_messages = {k: v for k, v in lint_messages.items() if v}
    return lint_messages

def fix_lint(file_path: str, messages: str) -> bool:
    """
    Invokes the chain to fix the given errors in the code and returns the fixed code and response.
    """
    full_path = os.path.join(config.get("dir"), file_path)
    attempt = 1
    with open(full_path, 'r') as file:
        original_code = file.read()
    while messages:
        with open(full_path, 'r') as file:
            file_contents = file.read()
        click.echo(f"Fixing lint issues in {file_path} (attempt {attempt})...")
        response = send_message('lint_fix', 
                                        {'code': file_contents, 
                                          'lint_issues': messages})
        response_messages = extract_messages(response)
        logger.info(f"Response messages: {response_messages}")
        fixed_code = extract_code(response)
        write_code_to_file(file_path=full_path, code=fixed_code)

        lint_result = execute_lint()
        errors = read_lint_output(lint_result)
        # check if error has been fixed
        if errors.get(file_path) is None:
            click.echo(f"{file_path} has no more lint issues.")
            click.echo(f"Fix successful after {attempt} attempts.")
            click.echo(" ")
            return True
        else:
            messages = errors[file_path]
            attempt += 1
        if attempt > 3:
            # restore to original code
            write_code_to_file(file_path=full_path, code=original_code)
            click.echo("Fix failed after 3 attempts.")
            return False
        