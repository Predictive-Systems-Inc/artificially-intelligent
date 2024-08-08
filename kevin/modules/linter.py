import json
import re
import subprocess
from typing import Any, Dict, List, Tuple
import os

from langchain.chat_models.base  import BaseChatModel

from modules.prompts import create_error_fetcher_rag_prompt, create_error_fixer_rag_prompt
from modules.utils import create_langchain, extract_code, write_code_to_file
from config import config

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
    filename = ""

    for line in output.splitlines():
        if "error" in line.lower():
            lint_messages[filename].append(line)
        elif "warning" in line.lower():
            lint_messages[filename].append(line)
        else:
            filename = line
            lint_messages[filename] = []
    # remove all empty lists
    lint_messages = {k: v for k, v in lint_messages.items() if v}
    return lint_messages

def fix_lint(code: str, messages: str, llm: BaseChatModel) -> Tuple[str, str]:
    """
    Invokes the chain to fix the given errors in the code and returns the fixed code and response.
    """
    chain = create_langchain(llm=llm, prompt=create_error_fixer_rag_prompt())
    response = chain.invoke(
        {
            "context": code,
            "question": f"Fix the errors/warnings: {messages} in the given code.",
        }
    )
    # print(response)
    fixed_code = extract_code(response)
    return fixed_code

def lint_and_fix(
    llm: BaseChatModel,
    project_dir: str,
    code: str,
    file_path: str,
    max_attempts: int = 3,
) -> str:
    """
    Lints the given code, fixes the errors, and writes the fixed code to a file.
    Returns the fixed code or the original code if no errors were found or the errors could not be fixed.
    """
    for attempt in range(max_attempts):
      print(f"Linting attempt {attempt + 1}...")
      lint_output = execute_lint(project_dir=project_dir)
      print("Linting complete. Getting errors...")
      errors = get_errors(lint_output=lint_output, file_path=file_path, llm=llm)
      print(errors)

      if errors == "No errors found." or errors == "I don't know.":
          print("No errors found. Skipping fix.")
          print("Updated code...")
          write_code_to_file(file_path=file_path, code=code)
          return code

      print("Fixing errors...")
      code = fix_errors(code=code, errors=errors, llm=llm)
      print("Updated code...")
      write_code_to_file(file_path=file_path, code=code)
    
    return code