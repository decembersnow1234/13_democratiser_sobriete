import os
import pandas as pd
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

# File names
iso_code_map = os.getenv("iso_code_map")
iso_country_code = os.getenv("iso_country_code")
carbon_neutrality_timeline = os.getenv("carbon_neutrality_timeline")
gdp_ppp_constant = os.getenv("gdp_ppp_constant")
population_timeline = os.getenv("population_timeline")
co2_emission_territory = os.getenv("co2_emission_territory")
co2_emission_consumption = os.getenv("co2_emission_consumption")

# Global carbon budgets
BUDGET_GLOBAL_lamboll_2C = {"33%": 1603000, "50%": 1219000, "67%": 944000}
BUDGET_GLOBAL_foster_2C = {"33%": 1450000, "50%": 1150000, "67%": 950000}
BUDGET_GLOBAL_lamboll_15C = {"33%": 480000, "50%": 247000, "67%": 60000}
BUDGET_GLOBAL_foster_15C = {"33%": 300000, "50%": 250000, "67%": 150000}

def get_global_budget(warming_scenario, probability, budget_source):
    if warming_scenario == '2°C':
        return BUDGET_GLOBAL_lamboll_2C[probability] if budget_source == 'Lamboll' else BUDGET_GLOBAL_foster_2C[probability]
    else:
        return BUDGET_GLOBAL_lamboll_15C[probability] if budget_source == 'Lamboll' else BUDGET_GLOBAL_foster_15C[probability]

def load_current_targets():
    path = os.path.join(DATA_DIR, carbon_neutrality_timeline)
    if not os.path.exists(path):
        print(f"Warning: current targets file not found at {path}. Returning empty dict.")
        return {}

    targets = pd.read_excel(path)
    iso_mapping = pd.read_excel(os.path.join(DATA_DIR, iso_code_map))
    iso_mapping.rename(columns={'Alpha-2 code': 'ISO2', 'Alpha-3 code': 'ISO3'}, inplace=True)

    eu_mapping = pd.read_excel(os.path.join(DATA_DIR, iso_country_code), sheet_name="G20_EU_Countries ", header=0)
    eu_mapping = eu_mapping.merge(iso_mapping, on='ISO3', how='left')
    eu_countries = eu_mapping[eu_mapping['EU_country'] == 'Yes']['ISO2'].tolist()

    target_mapping = {}
    for _, row in targets.iterrows():
        iso = row['ISO']
        target_year = row['Target year']

        if pd.notna(iso) and pd.notna(target_year):
            if iso == 'NGA' and target_year == '2050-2070':
                target_year = 2070
            elif isinstance(target_year, str):
                try:
                    target_year = int(target_year)
                except ValueError:
                    continue

            if iso == 'EU27':
                for eu_iso in eu_countries:
                    target_mapping[eu_iso] = int(target_year)
            else:
                target_mapping[iso] = int(target_year)

    return target_mapping

def create_base_dataframe(df):
    base_df = df[['ISO2', 'Country', 'Region']].drop_duplicates()
    pop_2050 = df[(df['Emissions_scope'] == 'Territory') & (df['Year'] == 2050)][['ISO2', 'Population']]
    pop_2050.rename(columns={'Population': 'Population_2050'}, inplace=True)

    world_pop_2050 = df[(df['Emissions_scope'] == 'Territory') & (df['Year'] == 2050) & (df['ISO2'] == 'WLD')]['Population'].iloc[0]
    base_df = base_df.merge(pop_2050, on='ISO2', how='left')
    base_df['Share_of_total_population_2050'] = base_df['Population_2050'] / world_pop_2050

    for scope in ['Territory', 'Consumption']:
        scope_data = df[
            (df['Emissions_scope'] == scope) &
            (df['Annual_CO2_emissions_Mt'].notna()) &
            (df['Annual_CO2_emissions_Mt'] != 0) &
            (df['Year'] != 2050)
        ]

        country_latest = scope_data[~scope_data['ISO2'].isin(['WLD', 'REG', 'EU', 'G20'])].groupby('ISO2')['Year'].max().reset_index()
        aggregate_latest = scope_data[scope_data['ISO2'].isin(['WLD', 'REG', 'EU', 'G20'])].groupby('ISO2')['Year'].max().reset_index()
        latest_years = pd.concat([country_latest, aggregate_latest])
        latest_years.columns = ['ISO2', f'Latest_year_{scope}']
        latest_years[f'Latest_year_{scope}'] = latest_years[f'Latest_year_{scope}'].astype(int)

        latest_data = pd.merge(scope_data, latest_years, left_on=['ISO2', 'Year'], right_on=['ISO2', f'Latest_year_{scope}'])[
            ['ISO2', 'Annual_CO2_emissions_Mt', 'Cumulative_CO2_emissions_Mt', 'Cumulative_population']
        ].rename(columns={
            'Annual_CO2_emissions_Mt': f'Latest_annual_CO2_emissions_Mt_{scope}',
            'Cumulative_CO2_emissions_Mt': f'Latest_cumulative_CO2_emissions_Mt_{scope}',
            'Cumulative_population': f'Latest_cumulative_population_{scope}'
        })

        base_df = base_df.merge(latest_years, on='ISO2', how='left')
        base_df = base_df.merge(latest_data, on='ISO2', how='left')

        world_cum_pop = base_df[base_df['ISO2'] == 'WLD'][f'Latest_cumulative_population_{scope}'].iloc[0]
        base_df[f'Share_of_cumulative_population_{scope}'] = base_df[f'Latest_cumulative_population_{scope}'] / world_cum_pop

    return base_df

def run_etl_scenarios(base_df, current_targets):
    scenarios = []
    for _, row in base_df.iterrows():
        for emissions_scope in ['Territory', 'Consumption']:
            for warming_scenario in ['1.5°C', '2°C']:
                for probability in ['33%', '50%', '67%']:
                    for budget_source in ['Lamboll', 'Foster']:
                        for distribution in ['Equality', 'Responsibility', 'Current_target']:
                            global_budget = get_global_budget(warming_scenario, probability, budget_source)

                            if distribution == 'Equality':
                                country_budget = global_budget * row['Share_of_total_population_2050']
                            elif distribution == 'Responsibility':
                                world_cumulative = base_df[base_df['ISO2'] == 'WLD'][f'Latest_cumulative_CO2_emissions_Mt_{emissions_scope}'].iloc[0]
                                total_available = global_budget + world_cumulative
                                country_cumulative = row[f'Latest_cumulative_CO2_emissions_Mt_{emissions_scope}']
                                country_budget = (total_available * row[f'Share_of_cumulative_population_{emissions_scope}']) - country_cumulative
                            else:  # Current_target
                                country_budget = None

                            latest_annual = row[f'Latest_annual_CO2_emissions_Mt_{emissions_scope}']
                            latest_year = row[f'Latest_year_{emissions_scope}']
                            neutrality_year = current_targets.get(row['ISO2']) if distribution == 'Current_target' else None

                            if distribution == 'Current_target' and neutrality_year is not None and pd.notna(latest_annual) and latest_annual > 0:
                                years_to_neutrality = neutrality_year - latest_year
                                country_budget = years_to_neutrality * latest_annual
                            # Here you might append to `scenarios` or write to file

    # return scenarios or process as needed
    print("ETL scenarios generated.")

if __name__ == "__main__":
    combined_df = pd.read_csv(os.path.join(OUTPUT_DIR, "combined_data.csv"))
    current_targets = load_current_targets()
    base_df = create_base_dataframe(combined_df)
    run_etl_scenarios(base_df, current_targets)
