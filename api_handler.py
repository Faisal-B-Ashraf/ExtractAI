import time
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.exceptions import OutputParserException

# Initialize the LLM
llm = OllamaLLM(model="llama3.3")
# llm = OllamaLLM(model="phi4")
# llm = OllamaLLM(model="gemma2")

# Initialize the JSON output parser
json_parser = JsonOutputParser()

# Initialize the output parser
output_parser = OutputFixingParser.from_llm(parser=json_parser, llm=llm)



def analyze_chunk(chunk, task):
    """
    Analyzes a chunk of text using the OpenAI API and handles throttling.
    """
    global dynamic_delay
    while True:
        try:
            prompt = ChatPromptTemplate.from_template(task)

            chain = prompt | llm | output_parser

            response = chain.invoke({"question": chunk})

            value, context = response['value'], response['context']

            return {"value": value, "context": context}

        except Exception as e:
            print(f"Error: {e}.")
            # return {"value": "Error", "context": f"{e}"}
            return {"value": "Error", "context": f"Error"}
