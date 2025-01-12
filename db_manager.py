import sqlite3

def create_or_update_table(db_path, task_names):
    """
    Ensures the structured_results table exists and dynamically updates its schema
    by adding value, context, and hash columns for all tasks.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS structured_results (dam_name TEXT PRIMARY KEY);"
    )

    # Get existing columns
    cursor.execute("PRAGMA table_info(structured_results);")
    existing_columns = {row[1] for row in cursor.fetchall()}

    # Add missing columns for each task
    for task_name in task_names:
        value_column = f"{task_name}_value"
        context_column = f"{task_name}_context"
        hash_column = f"{task_name}_hash"

        if value_column not in existing_columns:
            cursor.execute(f"ALTER TABLE structured_results ADD COLUMN {value_column} TEXT;")
        if context_column not in existing_columns:
            cursor.execute(f"ALTER TABLE structured_results ADD COLUMN {context_column} TEXT;")
        if hash_column not in existing_columns:
            cursor.execute(f"ALTER TABLE structured_results ADD COLUMN {hash_column} TEXT;")

    conn.commit()
    conn.close()

def insert_results(db_path, dam_name, results):
    """
    Inserts or updates results into the structured_results table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Dynamically generate the column names and placeholders
    columns = ", ".join(results.keys())
    placeholders = ", ".join(["?"] * len(results))
    query = f"INSERT OR REPLACE INTO structured_results (dam_name, {columns}) VALUES (?, {placeholders})"

    # Prepare the values for insertion
    values = [dam_name] + list(results.values())

    try:
        cursor.execute(query, values)
        conn.commit()
        print(f"Data for '{dam_name}' inserted/updated successfully.")
    except Exception as e:
        print(f"Error during insertion: {e}")
        raise e
    finally:
        conn.close()

def get_stored_task_data(db_path, dam_name):
    """
    Retrieve stored data and hashes for all tasks of a specific dam.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM structured_results WHERE dam_name = ?"
    cursor.execute(query, (dam_name,))
    row = cursor.fetchone()

    # Convert row into a dictionary if found
    if row:
        column_names = [description[0] for description in cursor.description]
        return dict(zip(column_names, row))
    return {}
