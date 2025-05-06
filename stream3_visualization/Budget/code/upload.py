"""import pandas as pd
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
"""
import pandas as pd
from sqlalchemy import create_engine
from config.paths import DATABASE_URL
from file_handler import get_file_path


class DatabaseUploader:
    """Handles uploading CSV files to a SQL database."""

    def __init__(self):
        """Initialize database engine."""
        self.engine = create_engine(DATABASE_URL)

    def upload_to_db(self, file_name, table_name):
        """Upload a single CSV file to the specified database table."""
        path = get_file_path(file_name)
        df = pd.read_csv(path, low_memory=False)
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        print(f"✅ Uploaded {file_name} → {table_name}")

    def upload_multiple(self, file_table_mapping):
        """Upload multiple CSV files to the database based on mapping."""
        for file_name, table_name in file_table_mapping.items():
            self.upload_to_db(file_name, table_name)

