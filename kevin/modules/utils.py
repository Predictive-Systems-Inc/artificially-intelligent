import os
import platform
import re
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Tuple

from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

def create_llm(model: str, api_version: str, azure_endpoint: str) -> AzureChatOpenAI:
    """
    Creates an instance of AzureChatOpenAI with the provided model, API version, and Azure endpoint.
    """
    return AzureChatOpenAI(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )

def create_langchain(llm: AzureChatOpenAI, prompt: ChatPromptTemplate):
    """
    Creates a LangChain instance with the provided LLM and prompt.
    """
    return (
        {"context": itemgetter("context"), "question": itemgetter("question")}
        | prompt | llm | StrOutputParser()
    )

def get_context_data(paths: List[str]) -> Dict[str, str]:
    """
    Reads the content of the specified files or all files in the specified directories
    and returns their content as a dictionary.

    :param paths: List of file or directory paths.
    :return: A dictionary with the combined content of all specified files.
    """
    data = {'data': ''}

    for path in paths:
        path_obj = Path(path)

        if not path_obj.exists():
            raise ValueError(f"Invalid path: {path_obj}")

        if path_obj.is_dir():
            # If the path is a directory, read all files in the directory
            for file_path in path_obj.glob('*'):
                if file_path.is_file():
                    content = file_path.read_text()
                    print(f"Reading file: {file_path}")
                    data['data'] += f"Example for {file_path.stem.upper()}:\n{content}\n"
        elif path_obj.is_file():
            # If the path is a file, read just that file
            content = path_obj.read_text()
            print(f"Reading file: {path_obj}")
            data['data'] += f"Example for {path_obj.stem.upper()}:\n{content}\n"
        else:
            raise ValueError(f"Path is neither a file nor a directory: {path_obj}")

    return data


def extract_messages(data: str) -> List[str]:
    """
    Extracts messages from the provided data.
    """
    # Remove the code blocks from the data
    data = re.sub(r"```(?:[a-z]*)\n([\s\S]*?)```", "...", data)
    return data

def extract_code(data: str) -> Tuple[str, str]:
    """
    Extracts the code from the provided data.
    """
    code_pattern = re.compile(r"```(?:[a-z]*)\n([\s\S]*?)```", re.MULTILINE)

    code_match = code_pattern.search(data)

    if code_match:
        code = code_match.group(1).strip()
    else:
        code = ''

    return code

def write_code_to_file(file_path: str, code: str) -> str:
    """
    Writes the provided code to the specified file path, overwriting it if it exists.
    """
    # print(file_path)
    # print(code)
    if not file_path or not code:
        raise ValueError("File path or code not provided")

    path = Path(file_path)
    os.makedirs(path.parent, exist_ok=True)
    path.write_text(code+"\n")
    print(f"Code written to {path}")

    return str(file_path)

def get_all_files(directory: str) -> List[str]:
    """
    Retrieves all files from the specified directory and its subdirectories,
    excluding certain folders and files based on their extensions.
    
    :param directory: The directory to search for files.
    :return: A list of file paths as strings.
    """
    path = Path(directory)

    if not path.exists() or not path.is_dir():
        print("Invalid location.")
        return []

    valid_extensions = {'.tsx', '.ts', '.prisma'}
    excluded_folders = {'node_modules', 'zod', 'generated'}
    
    return [
        str(file) for file in path.rglob('*')
        if file.is_file() and 
           file.suffix in valid_extensions and 
           not file.name.startswith('.') and
           not any(excluded_folder in file.parts for excluded_folder in excluded_folders) and
           not any(part.startswith('.') for part in file.parts if part != file.name)
    ]

def get_matching_files(files: List[str], search_input: str) -> List[str]:
    """
    Filters the list of files to return those that match or contain the search input.
    """
    return [file for file in files if search_input.lower() in file.lower()]

def list_all_subdirectories_and_files(path: str):
    """
    Lists all subdirectories and files of the specified path, excluding 'node_modules'
    and any directories starting with a dot.
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        raise ValueError(f"Invalid path: {path}")
    invalid_dirs = ['node_modules', 'common', 'ui', 'generated', 'zod', 'config-eslint', 'config-typescript']
    structure = {}
    for root, dirs, files in os.walk(path):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if not (d in invalid_dirs or d.startswith('.'))]
        
        # Add files to the structure
        rel_root = os.path.relpath(root, path)
        if rel_root == '.':
            rel_root = ''
        structure[rel_root] = {
            'subdirs': dirs,
            'files': files
        }
    return structure

def combine_structure_to_string(structure: Dict[str, Dict[str, List[str]]]) -> str:
    """
    Combines the directory structure into a single string.
    """
    result = []
    for dir_path, contents in structure.items():
        result.append(f"Directory: {dir_path}")
        if contents['subdirs']:
            result.append(f"  Subdirectories: {', '.join(contents['subdirs'])}")
        if contents['files']:
            result.append(f"  Files: {', '.join(contents['files'])}")
    
    return "\n".join(result)

def append_to_path(base_path, paths: List[str]):
    """
    Appends subdirectories or filenames to the base path in a cross-platform way.

    :param base_path: The base directory path as a string or Path object.
    :param paths: A list of additional path components to append to the base path.
    :return: The combined path as a Path object.
    """
    base_path = Path(base_path)
    return base_path.joinpath(*paths)

def clear_console():
    command = 'cls' if platform.system() == "Windows" else 'clear'
    os.system(command)

def display_options(options: List[str]) -> str:
    print("\nOptions:")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    return input("Enter choice: ")
