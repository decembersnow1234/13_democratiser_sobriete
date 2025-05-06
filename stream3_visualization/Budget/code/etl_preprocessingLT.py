import pandas as pd
import sys
import os

# Add the parent directory to the path (using raw string for the file path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'..')))
from config import filenames, budget_parameters


from utils.io import LoadData, DataAnalysis
from config import settings

def run_etl_preprocessing(DATA_DIR, OUTPUT_DIR, iso_code_map, iso_country_code, carbon_neutrality_timeline,
                           gdp_ppp_constant, population_timeline, co2_emission_territory, co2_emission_consumption):
    print("Running ETL Preprocessing...")
    population_data = pd.concat([historical_population_data, forecasted_population_data], ignore_index=True)

    iso2_mapping = iso_mapping.set_index('ISO3')['ISO2'].to_dict()
    population_data['ISO2'] = population_data['ISO3'].map(iso2_mapping)
    emissions_data['ISO2'] = emissions_data['ISO3'].map(iso2_mapping)
    consumption_emissions_data['ISO2'] = consumption_emissions_data['ISO3'].map(iso2_mapping)

    population_data.loc[population_data['ISO3'] == 'NAM', 'ISO2'] = 'NA'
    emissions_data.loc[emissions_data['ISO3'] == 'NAM', 'ISO2'] = 'NA'
    consumption_emissions_data.loc[consumption_emissions_data['ISO3'] == 'NAM', 'ISO2'] = 'NA'

    valid_iso3_codes = set(ipcc_regions['ISO3'].unique())
    emissions_data = emissions_data[emissions_data['ISO3'].isin(valid_iso3_codes)]
    consumption_emissions_data = consumption_emissions_data[consumption_emissions_data['ISO3'].isin(valid_iso3_codes)]

    region_mapping = ipcc_regions.set_index('ISO3')['IPCC_Region_Intermediate'].to_dict()
    emissions_data['Region'] = emissions_data['ISO3'].map(region_mapping)
    consumption_emissions_data['Region'] = consumption_emissions_data['ISO3'].map(region_mapping)

    eu_mapping = eu_g20_mapping.set_index('ISO3')['EU_country'].to_dict()
    g20_mapping = eu_g20_mapping.set_index('ISO3')['G20_country'].to_dict()

    emissions_data['EU_country'] = emissions_data['ISO3'].map(eu_mapping).fillna('No')
    emissions_data['G20_country'] = emissions_data['ISO3'].map(g20_mapping).fillna('No')
    consumption_emissions_data['EU_country'] = consumption_emissions_data['ISO3'].map(eu_mapping).fillna('No')
    consumption_emissions_data['G20_country'] = consumption_emissions_data['ISO3'].map(g20_mapping).fillna('No')

    base_df = population_data[population_data['ISO3'].isin(valid_iso3_codes)].copy()
    base_df['Region'] = base_df['ISO3'].map(region_mapping)
    base_df['EU_country'] = base_df['ISO3'].map(eu_mapping).fillna('No')
    base_df['G20_country'] = base_df['ISO3'].map(g20_mapping).fillna('No')

    territory_df = base_df.copy()
    territory_df['Emissions_scope'] = 'Territory'
    territory_df = territory_df.merge(
        emissions_data[['ISO3', 'Year', 'Annual_CO2_emissions_Mt']],
        on=['ISO3', 'Year'],
        how='left'
    )

    consumption_df = base_df.copy()
    consumption_df['Emissions_scope'] = 'Consumption'
    consumption_df = consumption_df.merge(
        consumption_emissions_data[['ISO3', 'Year', 'Annual_CO2_emissions_Mt']],
        on=['ISO3', 'Year'],
        how='left'
    )

    territory_df['Emissions_per_capita_ton'] = territory_df['Annual_CO2_emissions_Mt'] * 1000000 / territory_df['Population']
    consumption_df['Emissions_per_capita_ton'] = consumption_df['Annual_CO2_emissions_Mt'] * 1000000 / consumption_df['Population']

    emissions_df = pd.concat([territory_df, consumption_df], ignore_index=True)

    emissions_df['Cumulative_CO2_emissions_Mt'] = emissions_df.groupby(['ISO3', 'Region', 'Emissions_scope'])['Annual_CO2_emissions_Mt'].cumsum()
    emissions_df['Cumulative_population'] = emissions_df.groupby(['ISO3', 'Region', 'Emissions_scope'])['Population'].cumsum()

    world_aggregates = DataAnalysis.create_aggregates(emissions_df, ['Year', 'Emissions_scope'], 'All', 'WLD', 'World')

    region_aggregates = []
    for region in emissions_df['Region'].unique():
        if pd.notna(region):
            region_agg = DataAnalysis.create_aggregates(
                emissions_df[emissions_df['Region'] == region],
                ['Year', 'Emissions_scope'],
                'All',
                region,
                region
            )
            region_aggregates.append(region_agg)
    region_aggregates = pd.concat(region_aggregates, ignore_index=True)

    eu_aggregates = DataAnalysis.create_aggregates(
        emissions_df[emissions_df['EU_country'] == 'Yes'],
        ['Year', 'Emissions_scope'],
        'All',
        'EU',
        'European Union'
    )

    g20_aggregates = DataAnalysis.create_aggregates(
        emissions_df[emissions_df['G20_country'] == 'Yes'],
        ['Year', 'Emissions_scope'],
        'All',
        'G20',
        'G20 Countries'
    )
    # Add readable country names if possible
    iso3_to_country = iso_mapping.set_index('ISO3')['Country'].to_dict()
    emissions_df['Country'] = emissions_df['ISO3'].map(iso3_to_country)

    final_df = pd.concat([
        emissions_df,
        region_aggregates,
        world_aggregates,
        eu_aggregates,
        g20_aggregates
    ], ignore_index=True)

    for scope in ['Territory', 'Consumption']:
        world_cumulative_pop = world_aggregates[
            world_aggregates['Emissions_scope'] == scope
        ]['Cumulative_population'].iloc[0]
        final_df.loc[final_df['Emissions_scope'] == scope, 'Share_of_cumulative_population'] = (
            final_df[final_df['Emissions_scope'] == scope]['Cumulative_population'] / world_cumulative_pop
        )

    final_df = final_df[
        (final_df['Annual_CO2_emissions_Mt'].notna() & final_df['Annual_CO2_emissions_Mt'] != 0) |
        (final_df['Year'] == 2050)
    ]

    final_df = final_df.sort_values(['ISO3', 'Year', 'Emissions_scope'])
    final_df.to_csv(f"{OUTPUT_DIR}/combined_data.csv", index=False)

    print(f"Combined data saved to {OUTPUT_DIR}/combined_data.csv")
    print(f"Total rows: {len(final_df)}")
    print(f"Unique countries: {final_df['Country'].nunique()}")
    print(f"Year range: {final_df['Year'].min()} to {final_df['Year'].max()}")
    print(f"Emissions scopes: {', '.join(final_df['Emissions_scope'].unique())}")
    print(f"Added {len(region_aggregates)} region aggregate rows")
    print(f"Added {len(world_aggregates)} world aggregate rows")
    print(f"Added {len(eu_aggregates)} EU aggregate rows")
    print(f"Added {len(g20_aggregates)} G20 aggregate rows")
    print("\nFirst 50 rows of the combined dataframe:")
    print(final_df.head(50).to_string())


def process_combined_data():
    df = LoadData.read_csv("historical_emissions.csv")

    # keep only relevant columns
    df = df[["Country", "ISO2", "Region", "Sector", "Scope", "Year", "Annual_CO2_emissions_Mt"]]

    # calculate emissions per capita
    population_df = LoadData.read_csv("population.csv")
    df = df.merge(population_df[["ISO2", "Year", "Population"]], on=["ISO2", "Year"], how="left")
    df["Emissions_per_capita_ton"] = df["Annual_CO2_emissions_Mt"] * 1e6 / df["Population"]

    # cumulative emissions
    df["Cumulative_CO2_emissions_Mt"] = df.sort_values(by=["ISO2", "Year"]).groupby(["ISO2", "Scope"])["Annual_CO2_emissions_Mt"].cumsum()

    LoadData.save_csv(df, "combined_data.csv")
    return df
