# main.py
import pandas as pd
from utils.io import LoadData, DataAnalysis
from config import settings

df = pd.read_csv(f"{DATA_DIR}/{co2_emission_territory}")
targets = LoadData.load_current_targets()
base_df = DataAnalysis.create_base_dataframe(df)

combined = read_csv("combined_data.csv")
forecast = read_csv("forecast_data.csv")
parameters = read_csv("scenario_parameters.csv")

# Example usage:
budget = get_global_budget("1.5°C", "50%", "Lamboll")
print("Global 1.5°C 50% budget (Lamboll):", budget)




history, forecast, parameters = import_data()
if None in (history, forecast, parameters):
    return

print(f"Emission History after import: {history.columns}")
    print(f"Forecast after import: {forecast.columns}")
    print(f"Parameters after import: {parameters.columns}")

    history2, forecast2, parameters2 = reshape_data(history, forecast, parameters)

    print(f"Emission History after reshape: {history2.columns}")
    print(f"Forecast after reshape: {forecast2.columns}")
    print(f"Parameters after reshape: {parameters2.columns}")

    merged = parameters2.merge(forecast2, how="outer", on=["scenario_id"])
    to_be_concat = [merged, history2]
    result = concat(to_be_concat)

    print(f"Viz history forecast: {result.columns}")

    categorical_cols = ['Warming_scenario', 'Probability_of_reach',
                        'Budget_source', 'Budget_distribution_scenario', "Neutrality_year"]

    for col in categorical_cols:
        if col in result.columns:
            result[col] = result[col].astype(str).str.strip()

    result.to_csv(os.path.join(OUTPUT_DIR, "viz_history_forecast_data.csv"), index=False)
    print("viz_history_forecast.csv ready")

if __name__ == "__main__":
    main()

from processing.emissions import reshape_and_merge
from db.uploader import run_upload

if __name__ == "__main__":
    print("🚀 Starting data pipeline...")
    reshape_and_merge()
    run_upload()
    print("✅ Pipeline complete.")

from data.etl_processing import process_emissions
from data.etl_scenarios import process_scenario_forecasts
from data.merge_history_forecast import reshape_and_merge
from data.upload import upload_all

if __name__ == "__main__":
    print("🚀 Starting full carbon budget data pipeline...")

    process_emissions()
    process_scenario_forecasts()
    reshape_and_merge()
    upload_all()

    print("✅ Pipeline completed successfully.")
