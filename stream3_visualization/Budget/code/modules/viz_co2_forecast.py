import pandas as pd
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

def import_data():
    history_path = f"{OUTPUT_DIR}/combined_data.csv"
    forecast_path = f"{OUTPUT_DIR}/forecast_data.csv"
    parameters_path = f"{OUTPUT_DIR}/scenario_parameters.csv"

    try:
        history = pd.read_csv(history_path)
        forecast = pd.read_csv(forecast_path)
        parameters = pd.read_csv(parameters_path)
    except FileNotFoundError:
        print("Error: One or more files are missing.")
        return None, None, None

    return history, forecast, parameters

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
        #print(history.head())
        print(f"Emission History after import : ",history.columns)
        history2=history[['ISO2','Country', 'Region','Year',    'Emissions_scope', 
        'Annual_CO2_emissions_Mt',
       'Emissions_per_capita_ton', 'Cumulative_CO2_emissions_Mt',
       'Cumulative_population', 'Share_of_cumulative_population']]
        print(f"Emission History after reshape : ",history2.columns)
        #print(forecast.head())
        print(f"Forecast after import: ",forecast.columns)
        forecast['Annual_CO2_emissions_Mt']=forecast['Forecasted_emissions_Mt']
        forecast2=forecast.drop(columns='Forecasted_emissions_Mt')
        print(f"Forecast after reshape: ",forecast2.columns)
        #print(parameters.head())
        print(f"Parameters after import : ",parameters.columns)
        parameters=parameters[['ISO2', 'Country', 'Region', 'Emissions_scope', 'Warming_scenario',  
       'Probability_of_reach', 'Budget_source', 'Budget_distribution_scenario',      
              
       'Share_of_cumulative_population',
       'Population_2050', 'Share_of_total_population_2050',
        'scenario_id']]
        print(f"Parameters after reshape: ",parameters.columns)
        merged = process_forecast_data()
        to_be_concat=[merged,history2]
        result=concat(to_be_concat)
        #print(merged.head()) if merged is not None else print("No merged data available.")
        print(f"Viz history forecast ",result.columns)
        viz_history_forecast_df = result.to_csv(os.path.join(OUTPUT_DIR, "viz_history_forecast_data.csv"),index=False)
        print(f"viz_history_forecast.csv ready")
