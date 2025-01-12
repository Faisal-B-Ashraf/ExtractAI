from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Paths
DB_PATH = "D:/Oakridge/Projects/LLM/Database/processed_data.db"
PDF_FOLDER = "D:/Oakridge/Projects/LLM/All_Pdfs"

OUTPUT_FOLDER = "D:/Oakridge/Projects/LLM/Output"

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
