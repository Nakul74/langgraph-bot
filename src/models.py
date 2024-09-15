from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import os
import logger_config

# Load environment variables from .env file
load_dotenv()

# Configure the logger
logger = logger_config.get_logger(os.path.join('log_dir', 'logs.txt'))

try:
    # Initialize OpenAI Embeddings (use the correct model)
    openai_embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
    logger.info("OpenAI Embeddings initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing OpenAI Embeddings: {e}", exc_info=True)

try:
    # Initialize ChatOpenAI (adjust model name as needed)
    openai_llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # Replace with the appropriate model
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    logger.info("OpenAI LLM initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing OpenAI LLM: {e}", exc_info=True)
