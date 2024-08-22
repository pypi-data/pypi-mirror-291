import os
from openai import OpenAI
import pandas as pd
import glob
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_profiles():
    """Generate reports for database profiles based on CSV files."""
    csv_path = "./db/data/"
    profiles_path = "./db/profiles/"
    os.makedirs(csv_path, exist_ok=True)

    csv_files = glob.glob(os.path.join(csv_path, "*.csv"))
    total_files = len(csv_files)
    logging.info(f"Found {total_files} CSV files in {csv_path}.")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_csv_file, file, profiles_path, total_files, index) for index, file in enumerate(csv_files, start=1)]
        for future in as_completed(futures):
            future.result()  # To raise any exceptions that occurred during processing

def process_csv_file(file, profiles_path, total_files, index):
    """Process a CSV file and generate a report."""
    table_name = os.path.splitext(os.path.basename(file))[0]
    report_filename = os.path.join(profiles_path, f"{table_name}.md")

    if os.path.exists(report_filename):
        logging.info(f"Report for {table_name} already exists. Skipping... {index}/{total_files}")
        return

    data = pd.read_csv(file)
    logging.info(f"Generating report for {table_name} ({index}/{total_files})...")

    report = generate_report(table_name, data)

    os.makedirs(profiles_path, exist_ok=True)
    with open(report_filename, "w") as f:
        f.write(report)

    logging.info(f"Report for {table_name} saved as {report_filename}. {index}/{total_files} reports completed.")

def generate_report(table_name, data, rows=10):
    """Generate a detailed report for a given table."""
    prompt = f"""
    Generate a detailed profile for the table '{table_name}'. The table has the following sample data:
    {data.head(rows).to_string(index=False)}

    Include in the profile:
    - Headline. [# Table {table_name} profile]
    - A summary of the table's purpose based on the data. [## Overview] section
    - An analysis of the most significant columns and what they represent using a table with [name, description, string | number | ..., `sample_data` - some values separated by commas]. (## Columns)
    - Any notable patterns or insights observed from the sample data. [## Insights] section. For this section consider that the data you observe is just a sample, it's not representative of the entire dataset but it provides some shape visibility.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in data analysis."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192
        )

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"An error occurred while generating the report for {table_name}. Error: {e}")
        return generate_report(table_name, data, int(rows / 2))