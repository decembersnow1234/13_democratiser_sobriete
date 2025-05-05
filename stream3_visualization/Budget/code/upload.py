import pandas as pd
from sqlalchemy import create_engine
from config.settings import DATABASE_URL
from utils.io import get_file_path
from config import settings
engine = create_engine(DATABASE_URL)

def upload_to_db(file_name, table_name):
    path = get_file_path(file_name)
    df = pd.read_csv(path, low_memory=False)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ Uploaded {file_name} → {table_name}")

def upload_all():
    upload_to_db("combined_data.csv", "Viz_Carbon_Budget_combined_data_historical_Thao")
    upload_to_db("scenario_parameters.csv", "Viz_Carbon_Budget_scenario_parameters_Thao")
    upload_to_db("forecast_data.csv", "Viz_Carbon_Budget_forecast_data_Thao")
    upload_to_db("viz_history_forecast_data.csv", "Viz_Carbon_Budget_history_forecast_data_Thao")
