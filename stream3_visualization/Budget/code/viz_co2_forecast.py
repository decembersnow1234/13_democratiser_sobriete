import pandas as pd
from utils.io import read_csv, save_csv
from config import settings
def create_viz_history_forecast_data(combined,forecast,parameters):
    

    # forecast enrichment
    forecast['Annual_CO2_emissions_Mt'] = forecast['Forecasted_emissions_Mt']
    forecast = forecast.drop(columns='Forecasted_emissions_Mt')

    # combine historical and forecast
    history_df = combined[["Country", "ISO2", "Region", "Sector", "Scope", "Year",
                           "Annual_CO2_emissions_Mt", "Emissions_per_capita_ton", "Cumulative_CO2_emissions_Mt"]]

    # enrich forecast with params
    merged_forecast = forecast.merge(parameters, on="scenario_id", how="left")

    # select same structure for concatenation
    merged_forecast = merged_forecast.rename(columns={"Scope": "Emissions_scope"})
    history_df = history_df.rename(columns={"Scope": "Emissions_scope"})
    
    # merge both
    final_df = pd.concat([history_df, merged_forecast], ignore_index=True, sort=False)
    final_df = final_df.sort_values(by=["ISO2", "Year"]).reset_index(drop=True)

    save_csv(final_df, "viz_history_forecast_data.csv")
    return final_df
