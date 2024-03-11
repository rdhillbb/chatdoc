#
import os
import yaml
from typing import Any
# Assuming the correct import paths for your models
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.chat_models import ChatDeepInfra
from langchain_community.llms import DeepInfra
from langchain_groq import ChatGroq
#from langchain_anthropic import AnthropicLLM
#from langchain_community.chat_models import ChatAnthropic
#from langchain_community.chat_models import ChatAnthropic
from langchain_anthropic import ChatAnthropic
# Load YAML configuration
def load_config(config_file: str = "../config/llmparams.yaml") -> dict:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config.get("default", {})  # Fetch default config

# Mapping of model types to their corresponding classes
model_class_map = {
    "ChatOpenAI": ChatOpenAI,
    "OpenAI": OpenAI,
    "ChatDeepInfra": ChatDeepInfra,
    "DeepInfra": DeepInfra,
    "ChatGroq": ChatGroq,
    "AnthropicLLM":ChatAnthropic,
}
def get_llm(env_var: str = "GOVBOTIC_LLM") -> Any:

    llm_info = os.getenv(env_var)

    if not llm_info:
        raise ValueError(f"{env_var} environment variable is not set.")

    object_name, model_id = llm_info.split(":")
    if object_name not in model_class_map:
        raise ValueError(f"Unsupported object: {object_name}")

    config = load_config()  # Load configuration

    # Handle special case for DeepInfra
    if object_name == "DeepInfra":
        deepinfra_api_token = os.getenv("DEEPINFRA_API_TOKEN")
        if not deepinfra_api_token:
            raise ValueError("DEEPINFRA_API_TOKEN environment variable is not set.")
        llm = DeepInfra(model_id=model_id, deepinfra_api_token=deepinfra_api_token)
        model_kwargs = {k: v for k, v in config.items() if k not in ["model_id", "deepinfra_api_token"]}
        #llm.model_kwargs = model_kwargs
        #Will Address Later
        llm.model_kwargs = {
            "temperature": 0.2,
            "repetition_penalty": 1.2,
            "max_new_tokens": 8900,
            "top_p": 0.3,
        }

    # Add similar special handling for Anthropic
    elif object_name == "Anthropic":
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
        llm = ChatAnthropic(model=model_id, anthropic_api_key=anthropic_api_key)
        # Assuming Anthropic also uses model_kwargs or similar special settings
        model_kwargs = {k: v for k, v in config.items() if k not in ["model", "anthropic_api_key"]}
        llm.model_kwargs = model_kwargs

    else:
        # For other models, assume 'model_name' can be used and pass config directly
        llm = model_class_map[object_name](model_name=model_id, **config)
    print("Configuratioin")
    print("LLM",llm_info)
    print()
    return llm


# Function to instantiate and return the model object
def get_llmm(env_var: str = "GOVBOTIC_LLM") -> Any:
    print(env_var)
    llm_info = os.getenv(env_var)
    print(llm_info)
    if not llm_info:
        raise ValueError(f"{env_var} environment variable is not set.")

    object_name, model_id = llm_info.split(":")
    if object_name not in model_class_map:
        raise ValueError(f"Unsupported object: {object_name}")

    config = load_config()  # Load configuration

    if object_name == "DeepInfra":
        deepinfra_api_token = os.getenv("DEEPINFRA_API_TOKEN")
        if not deepinfra_api_token:
            raise ValueError("DEEPINFRA_API_TOKEN environment variable is not set.")

        # Instantiate DeepInfra with model_id and API token
        llm = DeepInfra(model_id=model_id, deepinfra_api_token=deepinfra_api_token)
        
        # Extract and assign model_kwargs from YAML config for DeepInfra
        model_kwargs = {k: v for k, v in config.items() if k not in ["model_id", "deepinfra_api_token"]}
        llm.model_kwargs = model_kwargs
    else:
        # For other models, assume 'model_name' can be used and pass config directly
        llm = model_class_map[object_name](model_name=model_id, **config)

    return llm
model_instance= ""
# Example usage
def set_modelInstance():
    global model_instance
    model_instance = get_llm()
    print(model_instance)
    return model_instance

def get_modelInstance():
    global model_instance
    return model_instance
set_modelInstance()
