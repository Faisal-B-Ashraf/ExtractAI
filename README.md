# ExtractAI

ExtractAI is a document processing pipeline designed to extract structured data from unstructured text in PDFs. It allows users to define custom tasks, prompts, and configurations to extract specific information efficiently.

---

## How to Use

### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Faisal-B-Ashraf/ExtractAI.git
```

### Set Up the Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Prepare Input Files

1. Place all your PDF files in a folder (e.g., `input_pdfs/`).
2. Update the `PDF_FOLDER` variable in `project_config.py` to point to the folder path:
   ```python
   PDF_FOLDER = "path/to/your/input_pdfs/"
   ```

### Configure the Database

Update the path to the SQLite database in `project_config.py`:
```python
DB_PATH = "path/to/processed_data.db"
```

---

## Customizing Tasks

Tasks define what data to extract from documents. They are configured in `task_definitions.py` and consist of:
- `task_name`: A unique identifier for the task.
- `system_message`: Instructions for the AI system to extract the desired information.
- `user_preamble`: A user-friendly description of the task.

### Example Task Definition:

```python
{
    "Dam_Name": {
        "system_message": "Extract the name of the dam from the text.",
        "user_preamble": "Identify the name of the dam mentioned in this document."
    },
    "Location": {
        "system_message": "Extract the location of the dam.",
        "user_preamble": "Provide the location of the dam as stated in the text."
    }
}
```

Add or edit tasks directly in `task_definitions.py` to customize the pipeline for your needs.

---

## Running the Pipeline

To process the documents and extract data, run:

```bash
python Main.py
```

---

## Output Structure

The extracted data is saved in a SQLite database. Each task generates a table with the following columns:

| Column     | Description                                                   |
|------------|---------------------------------------------------------------|
| task_name  | Name of the task (e.g., `Dam_Name`, `Location`, etc.).         |
| context    | The text/paragraph from which the value was derived.           |
| value      | The extracted data (e.g., `Bonneville Dam`, `Columbia River`). |

### Example Table (for `Dam_Name`):

| task_name | context                                                  | value            |
|-----------|----------------------------------------------------------|------------------|
| Dam_Name  | "The Bonneville Dam is located on the Columbia River..." | Bonneville Dam   |
| Dam_Name  | "Grand Coulee Dam is a key hydropower project..."         | Grand Coulee Dam |

This structure ensures users can trace the extracted values back to their source in the document.

---

## Folder Structure

Ensure the following structure for smooth operation:

```
ExtractAI/
├── Scripts for Git/
│   ├── Main.py
│   ├── api_handler.py
│   ├── db_manager.py
│   ├── pdf_processor.py
│   ├── task_definitions.py
│   ├── project_config.py
│   ├── requirements.txt
│   ├── .gitignore
├── All_Pdfs/  # Folder for input PDFs (ignored in .gitignore)
├── Database/  # Folder for database (ignored in .gitignore)
├── README.md
```

---

## Notes on Usage

- **Input PDFs:** Place all PDF files in the folder specified by `PDF_FOLDER`.
- **Database Updates:** If a document has already been processed, tasks will be skipped unless task definitions are modified.
- **Error Handling:** Errors during processing are logged, and other tasks will continue to execute.
