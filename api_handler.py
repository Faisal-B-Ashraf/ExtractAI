import openai
from project_config import OPENAI_API_KEY
import time
import math

openai.api_key = OPENAI_API_KEY

# Rolling token usage tracking
rolling_total_tokens = 0
request_count = 0
dynamic_delay = 0

def update_calibration(total_tokens, tpm_limit=200000):
    """
    Updates the rolling average of tokens per request and adjusts the delay dynamically.
    """
    global rolling_total_tokens, request_count, dynamic_delay

    # Update rolling totals
    request_count += 1
    rolling_total_tokens += total_tokens

    # Avoid division by zero
    if request_count == 0 or rolling_total_tokens == 0:
        dynamic_delay = 1  # Default delay
        print(f"Dynamic delay set to default: {dynamic_delay:.2f} seconds")
        return

    avg_tokens_per_request = rolling_total_tokens / request_count
    safe_requests_per_minute = max(1, math.floor(tpm_limit / avg_tokens_per_request))
    dynamic_delay = max(60 / safe_requests_per_minute, 0.5)

    # Log calibration details
    print(f"Total tokens used: {rolling_total_tokens}")
    print(f"Requests made: {request_count}")
    print(f"Average tokens per request: {avg_tokens_per_request:.2f}")
    print(f"Dynamic delay updated to: {dynamic_delay:.2f} seconds")

def analyze_chunk(chunk, task):
    """
    Analyzes a chunk of text using the OpenAI API and handles throttling.
    """
    global dynamic_delay
    while True:
        try:
            # Build the prompt
            prompt = f"{task['user_preamble']}{chunk}"
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": task["system_message"]},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )

            # Update calibration based on token usage
            total_tokens_used = len(prompt) + 200  # Add response token limit
            update_calibration(total_tokens_used)

            # Apply dynamic delay
            time.sleep(dynamic_delay)

            # Extract the content of the API response
            api_response = response['choices'][0]['message']['content']
            value, context = parse_response(api_response)
            return {"value": value, "context": context}

        except openai.error.RateLimitError:
            print("Rate limit reached. Retrying in 60 seconds...")
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(10)

def parse_response(api_response):
    """
    Parses the API response to extract value and context.
    """
    if "- Value:" in api_response and "- Context:" in api_response:
        value_start = api_response.find("- Value:") + len("- Value:")
        context_start = api_response.find("- Context:")
        value = api_response[value_start:context_start].strip()
        context = api_response[context_start + len("- Context:"):].strip()
        return value, context
    return api_response, ""
