from project_config import DB_PATH, PDF_FOLDER
from pdf_processor import extract_text_from_pdf, split_text_by_tokens
from api_handler import analyze_chunk
from db_manager import create_or_update_table, insert_results, get_stored_task_data
from task_definitions import get_prompts
import hashlib
import os

# Disable GPU - okay for inference
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def calculate_prompt_hash(task):
    """
    Calculate the hash of the task prompt.
    """
    # prompt_data = f"{task['system_message']}{task['user_preamble']}"
    prompt_data = task
    return hashlib.sha256(prompt_data.encode()).hexdigest()

def task_requires_reprocessing(stored_data, task_name, current_hash):
    """
    Determine if the task requires reprocessing based on stored data and hash.
    """
    stored_hash = stored_data.get(f"{task_name}_hash")
    stored_value = stored_data.get(f"{task_name}_value")
    return stored_hash != current_hash or not stored_value

def retain_existing_data(db_path, dam_name, structured_data):
    """
    Retrieves existing data for the dam and retains values for skipped tasks.
    """
    existing_data = get_stored_task_data(db_path, dam_name)
    if existing_data:
        for key, value in existing_data.items():
            # Only retain data if it's not already in the structured_data
            if key not in structured_data or not structured_data[key]:
                structured_data[key] = value
    return structured_data

def main():
    # Load task prompts
    prompts = get_prompts()
    task_names = prompts.keys()
    
    # Update database schema
    create_or_update_table(DB_PATH, task_names)
    
    # Process PDFs
    pdf_files = [file for file in os.listdir(PDF_FOLDER) if file.endswith('.pdf')]
    pdf_files = pdf_files[:2]
    
    if not pdf_files:
        print(f"No PDF files found in folder: {PDF_FOLDER}")
        return
    
    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file}")
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            print(f"No text extracted from {pdf_file}. Skipping...")
            continue

        # Split text into chunks
        chunks = split_text_by_tokens(text)
        # chunks = text
        # print(f"Number of chunks created for {pdf_file}: {len(chunks)}")

        structured_data = {}

        for chunk in chunks:  # Process each chunk
            dam_name = None  # Reset dam_name for each chunk

            # Process Dam_Name task
            dam_name_hash = calculate_prompt_hash(prompts["Dam_Name"])
            result = analyze_chunk(chunk, prompts["Dam_Name"])

            # task_value = result.get("value", "").strip()
            # task_context = result.get("context", "").strip()
            task_value = result['value']
            task_context = result['context']

            if task_value != 'Not mentioned':  # HJY - quick and dirty fix to avoid Dam name not found
                dam_name = task_value  # Set dam_name
                if dam_name not in structured_data:
                    structured_data[dam_name] = {"dam_name": dam_name}

                # Store Dam_Name results in structured_data
                structured_data[dam_name]["Dam_Name_value"] = task_value
                structured_data[dam_name]["Dam_Name_context"] = task_context
                structured_data[dam_name]["Dam_Name_hash"] = dam_name_hash

            # Skip further tasks if dam_name is not identified
            if not dam_name:
                print("Error: No dam_name identified for the chunk. Skipping tasks for this chunk.")
                continue

            # Retrieve stored data for the identified dam
            stored_data = get_stored_task_data(DB_PATH, dam_name)
            if stored_data:
                print(f"Stored data for dam '{dam_name}': {stored_data}")

            # Process other tasks
            for task_name, task in prompts.items():
                if task_name == "Dam_Name":
                    continue  # Skip Dam_Name; already handled

                # Check skipping logic for other tasks
                current_prompt_hash = calculate_prompt_hash(task)
                if stored_data and not task_requires_reprocessing(stored_data, task_name, current_prompt_hash):
                    print(f"Skipping task '{task_name}' for dam '{dam_name}'.")
                    continue

                # Process and store results
                try:
                    print(f"Reprocessing task '{task_name}' for dam '{dam_name}'.")
                    result = analyze_chunk(chunk, task)
                    # task_value = result.get("value", "").strip()
                    # task_context = result.get("context", "").strip()
                    task_value = result['value']
                    task_context = result['context']

                    structured_data[dam_name][f"{task_name}_value"] = task_value
                    structured_data[dam_name][f"{task_name}_context"] = task_context
                    structured_data[dam_name][f"{task_name}_hash"] = current_prompt_hash
                except Exception as e:
                    print(f"Error processing task {task_name}: {e}")

        # Retain existing data for skipped tasks
        for dam_name, results in structured_data.items():
            structured_data[dam_name] = retain_existing_data(DB_PATH, dam_name, structured_data[dam_name])

        # Insert structured data into the database
        for dam_name, results in structured_data.items():
            print(f"Inserting data for {dam_name}: {results}")
            insert_results(DB_PATH, dam_name, results)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()

