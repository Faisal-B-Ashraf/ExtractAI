# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 18:02:09 2025

@author: fbg
"""
pdf_files = pdf_files[:1]
import sqlite3

# Path to your database
db_path = "D:/Oakridge/Projects/LLM/Database/processed_data.db"


import sqlite3
import pandas as pd

# Paths
db_path = "D:/Oakridge/Projects/LLM/Database/processed_data.db"
output_csv_path = "D:/Oakridge/Projects/LLM/Output/structured_results.csv"

def export_database_to_csv(db_path, output_csv_path):
    """
    Export the contents of the structured_results table to a wide-format CSV file.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM structured_results"
        
        # Fetch data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Export DataFrame to CSV
        df.to_csv(output_csv_path, index=False)
        print(f"Data successfully exported to: {output_csv_path}")
    except Exception as e:
        print(f"Error exporting data to CSV: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_database_to_csv(db_path, output_csv_path)














import pandas as pd
import sqlite3

# Path to your database
db_path = "D:/Oakridge/Projects/LLM/Database/processed_data.db"

def load_database_to_dataframe(db_path):
    """
    Load the structured_results table into a pandas DataFrame for inspection.
    """
    conn = sqlite3.connect(db_path)
    try:
        # Load data into a DataFrame
        query = "SELECT * FROM structured_results"
        df = pd.read_sql_query(query, conn)
        print("Database loaded into DataFrame successfully.")
        return df
    except Exception as e:
        print(f"Error loading database: {e}")
    finally:
        conn.close()

# Load the data
df = load_database_to_dataframe(db_path)

# View the DataFrame in Variable Explorer
print(df)  # This prints the DataFrame in the console for quick inspection



























def drop_table(db_path):
    """
    Drops the structured_results table from the database if it exists.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS structured_results")
        conn.commit()
        print("Table 'structured_results' dropped successfully.")
    except Exception as e:
        print(f"Error dropping table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    drop_table(db_path)
