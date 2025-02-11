from project_config import DB_PATH, PDF_FOLDER
from pdf_processor import extract_text_from_pdf, split_text_by_tokens
from api_handler import analyze_chunk
from db_manager import create_or_update_table, insert_results, get_stored_task_data
from task_definitions import get_prompts
import pandas as pd
import hashlib
import os
import multiprocessing
import subprocess
import traceback

# Number of parallel processes for multiprocessing
NUM_PROCESSES = multiprocessing.cpu_count()

# Set the number of PDFs to process (comment out the next line to process all PDFs)
PDF_LIMIT = 1  # Change this number to process fewer PDFs or comment out to process all.

def test_ollama():
    """Check if Ollama is running by making a direct request."""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.3", "What is 2+2?"],
            capture_output=True, text=True, timeout=10
        )
        if "4" in result.stdout:
            print("✅ Ollama is running correctly!")
            return True
        else:
            print("🚨 Ollama response unexpected:", result.stdout)
            return False
    except Exception as e:
        print(f"🔥 Ollama test failed: {e}")
        return False

# Check if Ollama is running before processing
if not test_ollama():
    print("🚨 ERROR: Ollama is not responding! Restart it with: `ollama serve &`")
    exit(1)

def calculate_prompt_hash(task):
    """Calculate the hash of the task prompt."""
    return hashlib.sha256(task.encode()).hexdigest()

def generate_dynamic_fieldnames(prompts):
    """Dynamically generate field names based on available task definitions."""
    fieldnames = ["filename", "chunk"]
    for task_name in prompts.keys():
        fieldnames.extend([
            f"{task_name}_value",
            f"{task_name}_context",
            f"{task_name}_hash"
        ])
    return fieldnames

def save_results_to_dataframe(structured_data, fieldnames):
    """Convert structured data into a Pandas DataFrame for easy review."""
    df = pd.DataFrame.from_dict(structured_data, orient="index")
    df.reset_index(inplace=True)
    df.rename(columns={"index": "chunk"}, inplace=True)

    # Ensure DataFrame contains all expected columns
    for field in fieldnames:
        if field not in df.columns:
            df[field] = None

    return df

def process_chunk(chunk_data):
    """Process a single chunk of text with all tasks."""
    chunk_key, chunk_text, pdf_file, prompts = chunk_data
    chunk_results = {"filename": pdf_file, "chunk": chunk_key}

    for task_name, task in prompts.items():
        try:
            print(f"  Running task '{task_name}' on chunk {chunk_key}.")
            result = analyze_chunk(chunk_text, task)
            chunk_results[f"{task_name}_value"] = result["value"]
            chunk_results[f"{task_name}_context"] = result["context"]
            chunk_results[f"{task_name}_hash"] = calculate_prompt_hash(task)
        except Exception as e:
            print(f"🔥 ERROR processing task {task_name} for chunk {chunk_key}:\n{traceback.format_exc()}")
            chunk_results[f"{task_name}_value"] = "Error"
            chunk_results[f"{task_name}_context"] = str(e)

    return chunk_key, chunk_results

def main():
    prompts = get_prompts()
    fieldnames = generate_dynamic_fieldnames(prompts)
    pdf_folder = "./Faisal"
    pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

    if 'PDF_LIMIT' in globals() and isinstance(PDF_LIMIT, int):
        print(f"Limiting to the first {PDF_LIMIT} PDF file(s).")
        pdf_files = pdf_files[:PDF_LIMIT]
    else:
        print("Processing all PDF files in the folder.")

    if not pdf_files:
        print(f"No PDF files found in folder: {pdf_folder}")
        return

    structured_data = {}

    print(f"Processing {len(pdf_files)} PDF file(s)...")

    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file}")
        pdf_path = os.path.join(pdf_folder, pdf_file)
        text = extract_text_from_pdf(pdf_path)

        if not text:
            print(f"No text extracted from {pdf_file}. Skipping...")
            continue

        chunks = split_text_by_tokens(text)
        print(f"Split text into {len(chunks)} chunks for file: {pdf_file}.")

        chunk_data = [(f"chunk_{i+1}", chunks[i], pdf_file, prompts) for i in range(len(chunks))]

        with multiprocessing.Pool(NUM_PROCESSES) as pool:
            results = pool.map(process_chunk, chunk_data)

        for chunk_key, chunk_result in results:
            structured_data[chunk_key] = chunk_result

    df = save_results_to_dataframe(structured_data, fieldnames)

    import ace_tools as tools
    tools.display_dataframe_to_user(name="Extracted Data", dataframe=df)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
