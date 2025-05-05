from utils.io import LoadData, DataAnalysis
from config import settings
import os
import pandas as pd
from utils.io import get_global_budget


print("DATA_DIR:", DATA_DIR)
print("OUTPUT_DIR:", OUTPUT_DIR)
print("iso_code_map:", iso_code_map)


def run_etl_scenarios(base_df, current_targets):
    """Run ETL scenarios and generate forecast data."""
    try:
        # Create all scenario combinations
        scenarios = []
        for _, row in base_df.iterrows():
            for emissions_scope in ['Territory', 'Consumption']:
                for warming_scenario in ['1.5°C', '2°C']:
                    for probability in ['33%', '50%', '67%']:
                        for budget_source in ['Lamboll', 'Foster']:
                            for distribution in ['Equality', 'Responsibility', 'Current_target']:
                                # Calculate country carbon budget based on distribution scenario
                                global_budget = get_global_budget(warming_scenario, probability, budget_source)
                                if distribution == 'Equality':
                                    country_budget = global_budget * row['Share_of_total_population_2050']
                                elif distribution == 'Responsibility':
                                    # Get world's latest cumulative emissions
                                    world_cumulative = base_df[
                                        (base_df['ISO2'] == 'WLD') &
                                        (base_df[f'Latest_cumulative_CO2_emissions_Mt_{emissions_scope}'].notna())
                                    ][f'Latest_cumulative_CO2_emissions_Mt_{emissions_scope}'].iloc[0]

                                    # Calculate total available budget (global + world's historical emissions)
                                    total_available = global_budget + world_cumulative

                                    # Calculate country's share and subtract its historical emissions
                                    country_cumulative = row[f'Latest_cumulative_CO2_emissions_Mt_{emissions_scope}']
                                    country_budget = (total_available * row[f'Share_of_cumulative_population_{emissions_scope}']) - country_cumulative
                                else:  # Current_target
                                    country_budget = None

                                # Calculate years to neutrality and neutrality year
                                latest_annual = row[f'Latest_annual_CO2_emissions_Mt_{emissions_scope}']
                                latest_year = row[f'Latest_year_{emissions_scope}']

                                if distribution == 'Current_target':
                                    # Get target year from current targets mapping
                                    neutrality_year = current_targets.get(row['ISO2'])
                                    if neutrality_year is not None:
                                        years_to_neutrality = neutrality_year - latest_year
                                        # Back-calculate Country_carbon_budget based on years_to_neutrality
                                        if pd.notna(latest_annual) and latest_annual > 0:
                                            country_budget = (years_to_neutrality * latest_annual) / 2
                                        else:
                                            country_budget = None
                                    else:
                                        years_to_neutrality = "N/A"
                                        neutrality_year = "N/A"
                                        country_budget = None
                                elif pd.notna(country_budget) and pd.notna(latest_annual) and latest_annual > 0:
                                    years_to_neutrality = int(round(2 * country_budget / latest_annual))
                                    if years_to_neutrality + latest_year > 2100:
                                        neutrality_year = '>2100'
                                    elif  years_to_neutrality + latest_year < 2023:
                                        neutrality_year = '<2023'
                                    else:
                                        neutrality_year = int(round(latest_year + years_to_neutrality))
                                else:
                                    years_to_neutrality = 'N/A'
                                    neutrality_year = 'N/A'

                                scenario = {
                                    'ISO2': row['ISO2'],
                                    'Country': row['Country'],
                                    'Region': row['Region'],
                                    'Population_2050': row['Population_2050'],
                                    'Share_of_total_population_2050': row['Share_of_total_population_2050'],
                                    'Emissions_scope': emissions_scope,
                                    'Latest_year': latest_year,
                                    'Latest_annual_CO2_emissions_Mt': latest_annual,
                                    'Latest_cumulative_CO2_emissions_Mt': row[f'Latest_cumulative_CO2_emissions_Mt_{emissions_scope}'],
                                    'Latest_cumulative_population': row[f'Latest_cumulative_population_{emissions_scope}'],
                                    'Share_of_cumulative_population': row[f'Share_of_cumulative_population_{emissions_scope}'],
                                    'Warming_scenario': warming_scenario,
                                    'Probability_of_reach': probability,
                                    'Budget_source': budget_source,
                                    'Budget_distribution_scenario': distribution,
                                    'Global_Carbon_budget': global_budget,
                                    'Country_carbon_budget': country_budget,
                                    'Years_to_neutrality': years_to_neutrality,
                                    'Neutrality_year': neutrality_year
                                }
                                scenarios.append(scenario)

        # After creating the scenarios list, create two separate dataframes
        scenarios_df = pd.DataFrame(scenarios)
        print(f"Scenarios dataframe created with {len(scenarios_df)} rows.")
        scenario_params, forecast_df = split_files(scenarios_df)
        return scenario_params, forecast_df
    except Exception as e:
        print(f"Error running ETL scenarios: {e}")
        return pd.DataFrame(), pd.DataFrame()

def split_files(scenarios_df):
    """Split scenarios into scenario parameters and forecast data."""
    try:
        # 1. Create scenario parameters dataframe (one row per unique scenario)
        scenario_params = scenarios_df[[
            'ISO2', 'Country', 'Region', 'Emissions_scope',
            'Warming_scenario', 'Probability_of_reach', 'Budget_source',
            'Budget_distribution_scenario', 'Years_to_neutrality', 'Neutrality_year',
            'Latest_year', 'Latest_annual_CO2_emissions_Mt',
            'Latest_cumulative_CO2_emissions_Mt', 'Latest_cumulative_population',
            'Share_of_cumulative_population', 'Population_2050',
            'Share_of_total_population_2050', 'Global_Carbon_budget',
            'Country_carbon_budget'
        ]].drop_duplicates()

        # Create a scenario_id for each unique combination
        scenario_params['scenario_id'] = range(1, len(scenario_params) + 1)

        print(f"Scenario parameters dataframe created with {len(scenario_params)} rows.")

        # 2. Create forecast data dataframe
        forecast_data = []
        for _, row in scenario_params.iterrows():
            # Skip if no latest year or emissions data
            if pd.isna(row['Latest_year']) or pd.isna(row['Latest_annual_CO2_emissions_Mt']):
                continue

            # Convert years to integers
            latest_year = int(row['Latest_year'])

            # Handle different cases for forecast
            if (row['Years_to_neutrality'] == "N/A" or
                row['Years_to_neutrality'] is None or
                (isinstance(row['Years_to_neutrality'], (int, float)) and row['Years_to_neutrality'] <= 0)):
                # For N/A or negative years_to_neutrality, drop to zero immediately
                forecast_years = pd.DataFrame({
                    'Year': [latest_year + 1],
                    'Forecasted_emissions_Mt': [0]
                })
            else:
                # Normal case: linear decrease to zero
                if row['Neutrality_year'] == '>2100':
                    neutrality_year = 2100
                else:
                    neutrality_year = int(row['Neutrality_year'])
                forecast_years = pd.DataFrame({
                    'Year': range(latest_year + 1, neutrality_year + 1)
                })

                # Calculate forecasted emissions
                slope = -row['Latest_annual_CO2_emissions_Mt'] / (neutrality_year - latest_year)
                forecast_years['Forecasted_emissions_Mt'] = [
                    max(0, row['Latest_annual_CO2_emissions_Mt'] + slope * (year - latest_year))
                    for year in forecast_years['Year']
                ]

            # Add forecast data with scenario_id reference
            for _, year_row in forecast_years.iterrows():
                forecast_data.append({
                    'scenario_id': row['scenario_id'],
                    'Year': year_row['Year'],
                    'Forecasted_emissions_Mt': year_row['Forecasted_emissions_Mt']
                })

        # Convert forecast data to DataFrame
        forecast_df = pd.DataFrame(forecast_data)
        print(f"Forecast dataframe created with {len(forecast_df)} rows.")
        return scenario_params, forecast_df
    except Exception as e:
        print(f"Error splitting files: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Load the preprocessed data and current targets
combined_df = pd.read_csv(os.path.join(OUTPUT_DIR,"combined_data.csv"))
current_targets = LoadData.load_current_targets()

# Create the base dataframe
base_df = DataAnalysis.create_base_dataframe(combined_df)

# Run ETL scenarios and generate forecast data
scenario_params, forecast_df = run_etl_scenarios(base_df, current_targets)

# Save both files
scenario_params.to_csv(os.path.join(OUTPUT_DIR,"scenario_parameters.csv"), index=False)
forecast_df.to_csv(os.path.join(OUTPUT_DIR,"forecast_data.csv"), index=False)
#def main():
print(f"\nScenario parameters saved to {OUTPUT_DIR}/scenario_parameters.csv")
print(f"Forecast data saved to {OUTPUT_DIR}/forecast_data.csv")

#if __name__ == "__main__":
#    # this only runs if you execute the file directly
#    main()
