import pandas as pd
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

def import_data():
    history_path = os.path.join(OUTPUT_DIR, "combined_data.csv")
    forecast_path = os.path.join(OUTPUT_DIR, "forecast_data.csv")
    parameters_path = os.path.join(OUTPUT_DIR, "scenario_parameters.csv")

    print(f"Attempting to read files from: {OUTPUT_DIR}")
    print(f"History file path: {history_path}")
    print(f"Forecast file path: {forecast_path}")
    print(f"Parameters file path: {parameters_path}")

    try:
        # Check if files exist
        if not os.path.exists(history_path):
            print(f"Error: History file does not exist: {history_path}")
            return None, None, None
        if not os.path.exists(forecast_path):
            print(f"Error: Forecast file does not exist: {forecast_path}")
            return None, None, None
        if not os.path.exists(parameters_path):
            print(f"Error: Parameters file does not exist: {parameters_path}")
            return None, None, None

        # Check if files are empty
        if os.path.getsize(history_path) == 0:
            print(f"Error: History file is empty: {history_path}")
            return None, None, None
        if os.path.getsize(forecast_path) == 0:
            print(f"Error: Forecast file is empty: {forecast_path}")
            return None, None, None
        if os.path.getsize(parameters_path) == 0:
            print(f"Error: Parameters file is empty: {parameters_path}")
            return None, None, None

        # Read the files
        history = pd.read_csv(history_path)
        forecast = pd.read_csv(forecast_path)
        parameters = pd.read_csv(parameters_path)

        print("Files read successfully!")
        return history, forecast, parameters
    except Exception as e:
        print(f"Error reading files: {e}")
        return None, None, None

def process_forecast_data():
    history, forecast, parameters = import_data()

    if history is None or forecast is None or parameters is None:
        print("Error loading data. Exiting.")
        return None

    merged = parameters.merge(forecast, how="outer", on=["scenario_id"])
    return merged

def concat(to_be_concat):
    if not to_be_concat:
        print("Warning: No data to concatenate.")
        return None

    return pd.concat(to_be_concat, axis=0, ignore_index=True)

if __name__ == "__main__":
    history, forecast, parameters = import_data()

    if history is not None and forecast is not None and parameters is not None:
        print(f"Emission History after import: {history.columns}")
        history2 = history[['ISO2', 'Country', 'Region', 'Year', 'Emissions_scope',
                            'Annual_CO2_emissions_Mt', 'Emissions_per_capita_ton',
                            'Cumulative_CO2_emissions_Mt']]
        print(f"Emission History after reshape: {history2.columns}")

        print(f"Forecast after import: {forecast.columns}")
        forecast['Annual_CO2_emissions_Mt'] = forecast['Forecasted_emissions_Mt']
        forecast2 = forecast.drop(columns='Forecasted_emissions_Mt')
        print(f"Forecast after reshape: {forecast2.columns}")

        print(f"Parameters after import: {parameters.columns}")
        parameters = parameters[['ISO2', 'Country', 'Region', 'Emissions_scope', 'Warming_scenario',
                                 'Probability_of_reach', 'Budget_source', 'Budget_distribution_scenario',
                                 'scenario_id']]
        print(f"Parameters after reshape: {parameters.columns}")

        merged = process_forecast_data()
        to_be_concat = [merged, history2]
        result = concat(to_be_concat)
        print(f"Viz history forecast: {result.columns}")

        categorical_cols = ['Warming_scenario', 'Probability_of_reach',
                            'Budget_source', 'Budget_distribution_scenario', "Neutrality_year"]

        for col in categorical_cols:
            result[col] = result[col].astype(str).str.strip()

        viz_history_forecast_df = result.to_csv(os.path.join(OUTPUT_DIR, "viz_history_forecast_data.csv"), index=False)
        print(f"viz_history_forecast.csv ready")
