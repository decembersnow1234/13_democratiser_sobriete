import sys
import os
import pandas as pd
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

# Print environment variables for debugging
print("DATA_DIR:", DATA_DIR)
print("OUTPUT_DIR:", OUTPUT_DIR)

# File names
iso_code_map = os.getenv("iso_code_map")
iso_country_code = os.getenv("iso_country_code")
carbon_neutrality_timeline = os.getenv("carbon_neutrality_timeline")
gdp_ppp_constant = os.getenv("gdp_ppp_constant")
population_timeline = os.getenv("population_timeline")
co2_emission_territory = os.getenv("co2_emission_territory")
co2_emission_consumption = os.getenv("co2_emission_consumption")

# Append the correct path for the modules folder
modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Budget", "code", "modules"))
sys.path.append(modules_path)

# Print the modules path for debugging
print("Modules path:", modules_path)

# Import modules
try:
    import etl_preprocessing #import run_etl_preprocessing
    import etl_scenarios #import load_current_targets, create_base_dataframe, run_etl_scenarios, split_files
    #from etl_scenarios import create_base_dataframe, get_global_budget, load_current_targets
    import viz_co2_forecast #import process_forecast_data
    import upload #import run_upload
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def main():
    print("🚀 Running pipeline...")

    try:
        print("\n🔹 Running ETL Preprocessing...")
        print("Calling run_etl_preprocessing with the following parameters:")
        print("DATA_DIR:", DATA_DIR)
        print("OUTPUT_DIR:", OUTPUT_DIR)
        print("iso_code_map:", iso_code_map)
        print("iso_country_code:", iso_country_code)
        print("carbon_neutrality_timeline:", carbon_neutrality_timeline)
        print("gdp_ppp_constant:", gdp_ppp_constant)
        print("population_timeline:", population_timeline)
        print("co2_emission_territory:", co2_emission_territory)
        print("co2_emission_consumption:", co2_emission_consumption)

        etl_preprocessing.run_etl_preprocessing(DATA_DIR, OUTPUT_DIR, iso_code_map, iso_country_code, carbon_neutrality_timeline,
                              gdp_ppp_constant, population_timeline, co2_emission_territory, co2_emission_consumption)
        print("✅ ETL Preprocessing Complete!")

        # Verify the existence of combined_data.csv
        combined_data_path = os.path.join(OUTPUT_DIR, "combined_data.csv")
        if os.path.exists(combined_data_path):
            print(f"✅ combined_data.csv exists at {combined_data_path}")
        else:
            print(f"❌ combined_data.csv does not exist at {combined_data_path}")
            sys.exit(1)
    except Exception as e:
        print(f"Error in ETL Preprocessing: {e}")
        sys.exit(1)

    try:
        print("\n🔹 Running Scenarios Calculation...")
        print("🚀 Running ETL Scenario Pipeline...")

        print("\n🔹 Loading current targets...")
        current_targets = etl_scenarios.load_current_targets()
        print("✅ Current targets loaded!")

        print("\n🔹 Creating base dataframe...")
        combined_df = pd.read_csv(os.path.join(OUTPUT_DIR, "combined_data.csv"))
        base_df = etl_scenarios.create_base_dataframe(combined_df)
        print("✅ Base dataframe created!")

        print("\n🔹 Running ETL Scenarios...")
        scenarios_df = etl_scenarios.run_etl_scenarios(base_df, current_targets)
        scenario_params, forecast_df = etl_scenarios.split_files(scenarios_df)

        print("\n🔹 Saving scenario parameters and forecast data...")
        scenario_params.to_csv(os.path.join(OUTPUT_DIR, "scenario_parameters.csv"), index=False)
        forecast_df.to_csv(os.path.join(OUTPUT_DIR, "forecast_data.csv"), index=False)

        print("\n📂 Checking scenario_parameters.csv existence...")
        file_path = os.path.join(OUTPUT_DIR, "scenario_parameters.csv")
        print(f"Looking for: {file_path}")
        print("Exists? ", os.path.exists(file_path))
        print("✅ ETL Scenarios processed!")
    except Exception as e:
        print(f"Error in ETL Scenarios: {e}")
        sys.exit(1)

    try:
        print("\n🔹 Processing Forecast Data...")
        viz_co2_forecast.process_forecast_data()
        print("✅ Visualization Data Prepared!")
    except Exception as e:
        print(f"Error in Processing Forecast Data: {e}")
        sys.exit(1)

    try:
        print("\n🔹 Uploading to Database...")
        upload.run_upload()
        print("✅ Upload Complete!")
    except Exception as e:
        print(f"Error in Uploading to Database: {e}")
        sys.exit(1)

    print("\n🎉 All tasks completed successfully!")

if __name__ == "__main__":
    main()
