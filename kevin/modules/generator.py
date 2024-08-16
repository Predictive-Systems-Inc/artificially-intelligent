import os

from modules.llm import send_message, send_message_with_prompt
from config import config

import logging

from modules.utils import extract_code, extract_messages, write_code_to_file
logger = logging.getLogger(__name__)

def read_sources(template_dirs):
    # traverse all the directory and include all the files in the context
    context = {}
    base_dir = config.get('dir')
    for template_dir in template_dirs:
        template_dir = os.path.join(base_dir, template_dir)
        for root, _, files in os.walk(template_dir):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    context[file] = f.read()
    return context

def find_matching_files(keyword):
    # find all the files with the keyword in the project directory
    matching_files = []
    base_dir = config.get('dir')
    for root, _, files in os.walk(base_dir):
        for file in files:
            if keyword in file:
                matching_files.append(os.path.join(root, file))
    return matching_files

def _process_openai_response(response):
    # assumption: Filename are found in ### Filename: `<filename>`
    # assumption: Content are found in '''<content>''' after the filename
    files_created = []
    state = 0 # 0: finding filename, 1: finding start content 2: finding end content
    for message in response.split('\n'):
        if state == 0:
            if message.startswith('###'):
                filename = message.split(': ')[1].replace('`', '').strip()
                print(f"Creating file: {filename}")
                content = ""
                state = 1
            else:
                print(f"{message}")
        elif state == 1:
            if message.startswith("```"):
                # we ignore this line
                state = 2
            else:
                print(f"{message}")
        elif state == 2:
            if message.startswith("```"):
                # end of content, lets write the content to file
                file_path = os.path.join(config.get('dir') ,filename)
                print(f"Writing content to file: {file_path}")
                files_created.append(file_path)
                # create the folder if it does not exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(content)
                state = 0
            else:
                content += message + "\n"
    
    # process the response from the llm
    return files_created

def _process_llama_response(response):
    # process the response from the llm
    return 'Not supported yet...'

def perform_task(task, model):
    # generates the code based on the template and new model
    context = read_sources(task.get('sources'))
    context_str = ""
    for file, content in context.items():
        context_str += "Filename: " + file + "\n'''\n" + content + "\n'''\n\n"

    model_str = "Name: " + model.get('name') + "\n"
    for field in model.get('fields'):
        model_str += "Field: " + field.get('name') + ", " + field.get('type') + ", " + field.get('annotations') + "\n"
    prompt = task.get('prompt')
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Context: {context_str}")
    response = send_message_with_prompt(prompt, 
                              {'context': context_str, 
                               'model': model_str})
    logger.info(f"Response messages: {response}")
    # we need to generate the files recommended by the llm response
    print(config.get('llm'))
    if config.get('llm') == 'openai' or config.get('llm') == 'azure-openai':
        response = _process_openai_response(response)
    else:
        response = _process_llama_response(response)
    return response

def apply_change(file_path, instruction):
    # generates the code based on the template and new model
    with open(file_path, 'r') as f:
        code = f.read()
    code_str = "Filename: " + file_path + "\n'''\n" + code + "\n'''\n\n"
    
    logger.info(f"Instruction: {instruction}")
    logger.info(f"Code: {code_str}")
    response = send_message("update_code", 
                              {'code': code_str, 
                               'instruction': instruction})
    logger.info(f"Response messages: {response}")
    # we need to generate the files recommended by the llm response
    response_messages = extract_messages(response)
    logger.info(f"Response messages: {response_messages}")
    fixed_code = extract_code(response)
    result = write_code_to_file(file_path=file_path, code=fixed_code)
    return result

