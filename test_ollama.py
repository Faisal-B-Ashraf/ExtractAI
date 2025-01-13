import threading
import subprocess
import time

def run_ollama_serve():
    subprocess.Popen(["ollama", "serve"])
thread = threading.Thread(target=run_ollama_serve)
thread.start()
time.sleep(5)


from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.exceptions import OutputParserException


# Initialize the LLM
llm = OllamaLLM(model="llama3.3")

# Define the prompt template
template = """
system_message: You are an assistant that extracts the name of the dam, project, lock, or relevant structure mentioned in the document.
user_preamble:
    Extract the name of the dam, project, lock, or relevant structure explicitly mentioned in the text.
    Ensure your output strictly follows this JSON format:
    ```
    {{
        "value": "[Insert the name of the dam here]",
        "context": "[Provide any additional details or notes about the dam, if available]"
    }}
    ```
    Do not include any text outside this JSON object.
Question: {question}
"""

# Create the prompt
prompt = ChatPromptTemplate.from_template(template)

# Initialize the JSON output parser
json_parser = JsonOutputParser()

# Initialize the output parser
output_parser = OutputFixingParser.from_llm(parser=json_parser, llm=llm)

# Create the LLM chain with the prompt, model, and output parser
chain = prompt | llm | output_parser



# Define your queries
query1 = """
6. The Blue Lake Project includes three developments: (1) the Blue Lake
Development (located between stream miles 2.31 at Blue Lake dam and 0.32 at the Blue
Lake powerhouse); (2) the Fish Valve Unit (located about 1,900 feet downstream of the
Blue Lake dam); and (3) the Pulp Mill Feeder Unit (located just upstream from the Blue
Lake powerhouse). Water is discharged from the Blue Lake powerhouse, and the Fish Valve
and Pulp Mill Feeder units into the Sawmill Creek bypassed reach. The total length of
Sawmill Creek bypassed reach (from Blue Lake dam to Blue Lake powerhouse) is over 10,000 feet.
"""

query2 = """
17. Under section 307(c)(3)(A) of the Coastal Zone Management Act (CZMA), the Commission
cannot issue a license for a project within or affecting a state’s coastal zone unless the
state CZMA agency concurs with the license applicant’s certification of consistency with the
state’s CZMA program, or the agency’s concurrence is conclusively presumed by its failure
to act within 180 days of its receipt of the applicant’s certification.
"""

# Invoke the chain with the queries
try:
    response = chain.invoke({"question": query1})
    print(response)
except OutputParserException as e:
    print(f"Failed to parse output: {e}")

try:
    response = chain.invoke({"question": query2})
    print(response)
except OutputParserException as e:
    print(f"Failed to parse output: {e}")
