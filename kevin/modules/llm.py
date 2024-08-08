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

def send_message(template: str, message: str):
    """
    Sends a message to the AI model using the specified template.
    """
    # Retrieves the messages for the specified template
    # Find the prompt with key 'template' in the prompts
    messages = prompts.get(template)
    if messages is None:
        return f"ERROR: Template not found: {template}"

    # Creates a chat prompt from the messages
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    # Retrieves the LLM from the model config
    llm = ModelConfig.get_model()
    # Creates a chain of chat models to process the message
    chat_chain = chat_prompt | llm | StrOutputParser()
    # Invokes the chain with the message
    return chat_chain.invoke({"human": message})