import os
import pandas as pd

from code import file_handler
from config import OUTPUT_DIR
from code.etl_preprocess import ETLProcessor
from code.combined_data_processor import CombinedDataProcessor
from code.scenario_generator import ScenarioGenerator
from code.forecast_processor import ForecastProcessor
from code.viz_co2_forecast import VisualizationDataProcessor
from code.upload import DatabaseUploader

def process_etl_pipeline():
    """Run the ETL data preprocessing pipeline."""
    print("🚀 Running ETL preprocessing...")
    etl = ETLProcessor()
    processed_data = etl.preprocess()
    
    combined_processor = CombinedDataProcessor()
    final_data = combined_processor.process_combined_data()

    print("✅ ETL processing completed!")
    return final_data

def generate_forecast():
    """Generate forecast scenarios."""
    print("🚀 Generating forecast scenarios...")
    base_df = LoadData.read_csv("base_data.csv")
    current_targets = LoadData.read_csv("current_targets.csv").set_index("ISO2").to_dict()

    scenario_gen = ScenarioGenerator(base_df, current_targets)
    scenarios_df = scenario_gen.generate_scenarios()

    forecast_df = ForecastProcessor.generate_forecast(scenarios_df)
    
    print("✅ Scenario forecast generation completed!")
    return forecast_df

def process_visualization_data():
    """Merge historical and forecast data for visualization."""
    print("🚀 Processing visualization data...")
    combined_data = read_csv("combined_data.csv")
    forecast_data = read_csv("forecast_data.csv")
    parameters = read_csv("scenario_parameters.csv")

    viz_processor = VisualizationDataProcessor(combined_data, forecast_data, parameters)
    final_data = viz_processor.process()

    print("✅ Visualization data processing completed!")
    return final_data

def upload_data():
    """Upload processed data to the database."""
    print("🚀 Uploading data to the database...")
    uploader = DatabaseUploader()

    file_table_mapping = {
        "combined_data.csv": "Viz_Carbon_Budget_combined_data_historical_Thao",
        "scenario_parameters.csv": "Viz_Carbon_Budget_scenario_parameters_Thao",
        "forecast_data.csv": "Viz_Carbon_Budget_forecast_data_Thao",
        "viz_history_forecast_data.csv": "Viz_Carbon_Budget_history_forecast_data_Thao"
    }

    uploader.upload_multiple(file_table_mapping)
    print("✅ Data upload completed!")

def run_full_pipeline():
    """Run the complete carbon budget data pipeline."""
    print("🚀 Starting full carbon budget data pipeline...")
    
    etl_data = process_etl_pipeline()
    forecast_data = generate_forecast()
    visualization_data = process_visualization_data()
    upload_data()

    print("✅ Full pipeline execution completed!")

if __name__ == "__main__":
    run_full_pipeline()
