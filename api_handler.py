import time
import traceback
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.exceptions import OutputParserException

# Initialize the LLM with explicit base_url
llm = OllamaLLM(model="llama3.3", base_url="http://127.0.0.1:11434")

# Initialize the JSON output parser
json_parser = JsonOutputParser()
output_parser = OutputFixingParser.from_llm(parser=json_parser, llm=llm)

def analyze_chunk(chunk, task):
    """
    Analyzes a chunk of text using the LLM API and handles errors.
    """
    try:
        prompt = ChatPromptTemplate.from_template(task)
        chain = prompt | llm | output_parser
        response = chain.invoke({"question": chunk})

        value, context = response.get('value', 'Error'), response.get('context', 'No context available')

        return {"value": value, "context": context}

    except OutputParserException as e:
        print(f"🔥 ERROR (OutputParserException): {e}")
        print(traceback.format_exc())
        return {"value": "Error", "context": f"OutputParserException: {e}"}

    except Exception as e:
        print(f"🔥 ERROR (General Exception): {e}")
        print(traceback.format_exc())
        return {"value": "Error", "context": f"Exception: {e}"}
