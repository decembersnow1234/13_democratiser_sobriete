import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv



load_dotenv()  # Load environment variables from .env file
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ ERROR: DATABASE_URL is not set. Please check your .env file.")

engine = create_engine(DATABASE_URL)


def upload_to_db(file_name, table_name):
    path = os.path.join(OUTPUT_DIR, file_name)
    df = pd.read_csv(path,low_memory=False)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"{file_name} uploaded to {table_name}")

def run_upload():
    upload_to_db("combined_data.csv", "Viz_Carbon_Budget_combined_data_historical_Thao")
    upload_to_db("scenario_parameters.csv", "Viz_Carbon_Budget_scenario_parameters_Thao")
    upload_to_db("forecast_data.csv", "Viz_Carbon_Budget_forecast_data_Thao")
    upload_to_db("viz_history_forecast_data.csv", "Viz_Carbon_Budget_history_forecast_data_Thao")

if __name__ == "__main__":
    run_upload()
