import json
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter

from config import ModelConfig

prompts = None

def initialize_prompts():
    global prompts
    with open('templates/prompts.json', 'r') as f:
        prompts = json.load(f)
    # convert the list of dictionaries to a list of tuples
    for key, value in prompts.items():
        for i, entry in enumerate(value):
            prompts[key][i] = tuple(entry.items())[0]
    return prompts

# Initialize the config when the module is imported
initialize_prompts()

def send_message_with_prompt(prompt: str, args: dict):
    merged_messages = []
    for message in prompt:
        # if message[1] is a list, join the list into a string
        if isinstance(message, dict):
            message = tuple(message.items())[0]
        merged_messages.append(message)

    # # Creates a chat prompt from the messages
    chat_prompt = ChatPromptTemplate.from_messages(merged_messages)
    # Retrieves the LLM from the model config
    llm = ModelConfig.get_model()
    # Creates a chain of chat models to process the message
    chat_chain = chat_prompt | llm | StrOutputParser()
    # Invokes the chain with the message
    response = chat_chain.invoke(args)
    return response

def send_message(template: str, args: dict):
    """
    Sends a message to the AI model using the specified template and argument
    """
    # Retrieves the messages for the specified template
    # Find the prompt with key 'template' in the prompts
    prompt = prompts.get(template)
    if prompt is None:
        return f"ERROR: Template not found: {template}"
    
    return send_message_with_prompt(prompt, args)

    