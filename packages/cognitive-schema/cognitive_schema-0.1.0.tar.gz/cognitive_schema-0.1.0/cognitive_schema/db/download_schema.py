import psycopg2
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_schema(dbname, user, password, host, port):
    """Connect to the database and download the schema and sample data."""
    logging.info("Establishing connection to the database.")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    logging.info("Connection established.")

    # Query for schema
    schema_query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM
        information_schema.columns
    WHERE
        table_schema = 'public';
    """

    # Fetch the schema
    logging.info("Fetching the schema.")
    schema_df = pd.read_sql(schema_query, conn)
    logging.info("Schema fetched successfully.")

    # Fetch sample data for each table
    sample_data = {}
    total_tables = len(schema_df['table_name'].unique())
    for index, table in enumerate(schema_df['table_name'].unique(), start=1):
        logging.info(f"Fetching sample data for table: {table} ({index}/{total_tables})")
        sample_query = f"SELECT * FROM {table} LIMIT 1000;"
        sample_data[table] = pd.read_sql(sample_query, conn)
        logging.info(f"Sample data for table {table} fetched successfully. Remaining: {total_tables - index}")

    # Close the connection
    logging.info("Closing the connection.")
    conn.close()
    logging.info("Connection closed.")

    # Ensure the directories exist
    os.makedirs("db", exist_ok=True)
    os.makedirs("db/data", exist_ok=True)

    # Save schema and sample data to CSV files
    logging.info("Saving schema and sample data to CSV files.")
    schema_df.to_csv("db/database_schema.csv", index=False)
    for table, data in sample_data.items():
        data.to_csv(f"db/data/{table}.csv", index=False)
    logging.info("Schema and sample data saved to CSV files successfully.")