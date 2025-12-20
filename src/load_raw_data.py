# load_raw_data.py
import os
import time
import pandas as pd
import logging
from sqlalchemy import create_engine

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Logging setup
logging.basicConfig(
    filename="logs/load_raw_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# DB engine
engine = create_engine("sqlite:///project.db")

def ingest_db(df: pd.DataFrame, table_name: str):
    """Ingest DataFrame into SQLite database (project.db)."""
    df.to_sql(
        table_name,
        con=engine,
        if_exists='replace',
        index=False,
        method="multi",
        chunksize=10000
    )

def load_raw_data(folder_path: str):
    """Load all CSVs from folder into DB"""
    start_time = time.time()
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            logging.info(f"Reading file: {file}")
            df = pd.read_csv(file_path)
            logging.info(f"File loaded: {file} | Shape: {df.shape}")
            ingest_start = time.time()
            ingest_db(df, file[:-4])  # filename without .csv as table name
            ingest_end = time.time()
            logging.info(f"Uploaded {file} in {round(ingest_end - ingest_start, 2)} seconds.")
    logging.info(f"Ingestion complete in {round(time.time() - start_time, 2)} seconds.")

if __name__ == "__main__":
    folder_path = r"C:\Users\ASUS\Desktop\python code for my project\Project\Raw data\data"
    load_raw_data(folder_path)
