import json
import os

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv

load_dotenv()
config = None

def initialize_config():
    global config
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

# Initialize the config when the module is imported
initialize_config()

class ModelConfig:
    """
    A class to manage the global model configuration.
    """
    current_model: BaseChatModel = None
    temperature: float = 0.0

    @classmethod
    def initialize_model(cls):
        model_name = config.get("llm")
        if model_name == "openai":
            model = os.getenv("OPENAI_API_MODEL")
            cls.current_model = ChatOpenAI(model=model,
                                           temperature=cls.temperature)
        elif model_name == "azure-openai":
            cls.current_model = AzureChatOpenAI(
                                           temperature=cls.temperature,
                                           model=os.getenv("AZURE_OPENAI_API_MODEL"),
                                           api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
                                           azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'))
        elif model_name == "ollama":            
            cls.current_model = OllamaLLM(model=os.getenv("OLLAMA_MODEL"))
        else:
            raise ValueError(f"Invalid model name: {model_name}")
    
    @classmethod
    def update_temperature(cls, temperature: float):
        cls.temperature = temperature
        ModelConfig.initialize_model()
        
    @classmethod
    def get_model(cls) -> BaseChatModel:
        if cls.current_model is None:
            raise ValueError("Model not set. Call set_model() first.")
        return cls.current_model