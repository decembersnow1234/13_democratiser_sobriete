import os
import pandas as pd
from config import settings
from config.settings import OUTPUT_DIR
class Noname:
    @staticmethod
    def save_csv(df, file_name):
        path = LoadData.get_file_path(file_name)
        df.to_csv(path, index=False)
        print(f"✅ Saved: {file_name}")

    
class DataAnalysis:
    @staticmethod
    def create_measure_dataframe(df, measure_name, value_column):
        """Create a standardized measure dataframe."""
        measure_df = df.copy()
        measure_df['Measure'] = measure_name
        measure_df.rename(columns={value_column: 'Value'}, inplace=True)
        return measure_df[['ISO2', 'Country', 'Year', 'Measure', 'Value']]

    @staticmethod
    def calculate_derived_metrics(df):
        """Calculate per capita metrics."""
        df['Emissions_per_capita_ton'] = df['Annual_CO2_emissions_Mt'] * 1000000 / df['Population']
        return df

    @staticmethod
    def calculate_cumulative_emissions(df):
        """Calculate cumulative emissions for each country and scope."""
        df['Cumulative_CO2_emissions_Mt'] = df.groupby(['ISO2', 'Region'])['Annual_CO2_emissions_Mt'].cumsum()
        df['Cumulative_Consumption_CO2_emissions_Mt'] = df.groupby(['ISO2', 'Region'])['Consumption_CO2_emissions_Mt'].cumsum()
        return df

    @staticmethod
    def create_aggregates(df, group_cols, agg_name, iso_code, region_name):
        """Create aggregates for regions, world, EU, or G20."""
        aggregates = df.groupby(group_cols).agg({
            'Annual_CO2_emissions_Mt': 'sum',
            'Cumulative_CO2_emissions_Mt': 'sum',
            'Population': 'sum',
            'Cumulative_population': 'sum'
        }).reset_index()
        aggregates['Emissions_per_capita_ton'] = aggregates['Annual_CO2_emissions_Mt'] * 1000000 / aggregates['Population']
        aggregates['ISO2'] = iso_code
        aggregates['ISO3'] = iso_code
        aggregates['Country'] = agg_name
        aggregates['Region'] = region_name
        aggregates['EU_country'] = 'N/A'
        aggregates['G20_country'] = 'N/A'
        return aggregates
    
    @staticmethod
    def get_global_budget(warming_scenario, probability, budget_source):
        """Get the global carbon budget based on scenario parameters."""
        if warming_scenario == '2°C':
            if budget_source == 'Lamboll':
                return BUDGET_GLOBAL_lamboll_2C[probability]
            else:  # Foster
                return BUDGET_GLOBAL_foster_2C[probability]
        else:  # 1.5°C
            if budget_source == 'Lamboll':
                return BUDGET_GLOBAL_lamboll_15C[probability]
            else:  # Foster
                return BUDGET_GLOBAL_foster_15C[probability]

    @staticmethod
    def load_current_targets():
        """Load and process current target years."""
        try:
            # Load the current targets file
            targets = pd.read_excel(os.path.join(DATA_DIR,carbon_neutrality_timeline))
            print("Current targets loaded:", len(targets))

            # Load the ISO codes mapping file
            iso_mapping = pd.read_excel(os.path.join(DATA_DIR,iso_code_map))
            iso_mapping.rename(columns={'Alpha-2 code': 'ISO2', 'Alpha-3 code': 'ISO3'}, inplace=True)

            # Get EU countries mapping
            eu_mapping = pd.read_excel(os.path.join(DATA_DIR,iso_country_code),
                                    sheet_name="G20_EU_Countries ",
                                    header=0)

            # Merge ISO2 codes into the EU mapping
            eu_mapping = eu_mapping.merge(iso_mapping, on='ISO3', how='left')

            # Get EU countries with ISO2 codes
            eu_countries = eu_mapping[eu_mapping['EU_country'] == 'Yes']['ISO2'].tolist()

            # Create target mapping
            target_mapping = {}

            # Process each row
            for _, row in targets.iterrows():
                iso = row['ISO']
                target_year = row['Target year']

                if pd.notna(iso) and pd.notna(target_year):
                    # Handle special case for NGA
                    if iso == 'NGA' and target_year == '2050-2070':
                        target_year = 2070
                    elif isinstance(target_year, str):
                        try:
                            target_year = int(target_year)
                        except ValueError:
                            continue  # Skip if can't convert to integer

                    if iso == 'EU27':
                        # Add all EU countries with the same target year
                        for eu_iso in eu_countries:
                            target_mapping[eu_iso] = int(target_year)
                    else:
                        target_mapping[iso] = int(target_year)

            return target_mapping

        except Exception as e:
            print(f"Error loading current targets: {e}")
            return {}

    @staticmethod
    def create_base_dataframe(df):
        """Create base dataframe with required columns."""
        try:
            # Get unique countries and their regions
            base_df = df[['ISO2', 'Country', 'Region']].drop_duplicates()
            print("Base dataframe shape:", base_df.shape)

            # Get population data for 2050
            pop_2050 = df[
                (df['Emissions_scope'] == 'Territory') &  # Using Territory scope since population is the same
                (df['Year'] == 2050)
            ][['ISO2', 'Population']].rename(columns={'Population': 'Population_2050'})

            # Get world population for 2050
            world_pop_2050 = df[
                (df['Emissions_scope'] == 'Territory') &  # Using Territory scope since population is the same
                (df['Year'] == 2050) &
                (df['ISO2'] == 'WLD')
            ]['Population'].iloc[0]

            # Merge population data
            base_df = base_df.merge(pop_2050, on='ISO2', how='left')

            # Calculate share of total population
            base_df['Share_of_total_population_2050'] = base_df['Population_2050'] / world_pop_2050

            # Get latest year and emissions for each scope
            emission_scopes = ['Territory', 'Consumption']
            for scope in emission_scopes:
                # Filter data for this scope and where Annual_CO2_emissions_Mt is not null and not 0
                scope_data = df[
                    (df['Emissions_scope'] == scope) &
                    (df['Annual_CO2_emissions_Mt'].notna()) &
                    (df['Annual_CO2_emissions_Mt'] != 0) &
                    (df['Year'] != 2050)  # Exclude 2050 from latest year calculation
                ]

                # For regular countries, get latest year with emissions data
                country_latest_years = scope_data[
                    ~scope_data['ISO2'].isin(['WLD', 'REG', 'EU', 'G20'])
                ].groupby('ISO2')['Year'].max().reset_index()

                # For aggregates, get latest year with emissions data
                aggregate_latest_years = scope_data[
                    scope_data['ISO2'].isin(['WLD', 'REG', 'EU', 'G20'])
                ].groupby('ISO2')['Year'].max().reset_index()

                # Combine the latest years
                latest_years = pd.concat([country_latest_years, aggregate_latest_years])
                latest_years.columns = ['ISO2', f'Latest_year_{scope}']
                # Convert years to integers
                latest_years[f'Latest_year_{scope}'] = latest_years[f'Latest_year_{scope}'].astype(int)

                # Get latest emissions and population for each ISO2
                latest_data = pd.merge(
                    scope_data,
                    latest_years,
                    left_on=['ISO2', 'Year'],
                    right_on=['ISO2', f'Latest_year_{scope}']
                )[['ISO2', 'Annual_CO2_emissions_Mt', 'Cumulative_CO2_emissions_Mt', 'Cumulative_population']].rename(
                    columns={
                        'Annual_CO2_emissions_Mt': f'Latest_annual_CO2_emissions_Mt_{scope}',
                        'Cumulative_CO2_emissions_Mt': f'Latest_cumulative_CO2_emissions_Mt_{scope}',
                        'Cumulative_population': f'Latest_cumulative_population_{scope}'
                    }
                )

                # Merge with base dataframe
                base_df = base_df.merge(latest_years, on='ISO2', how='left')
                base_df = base_df.merge(latest_data, on='ISO2', how='left')

                # Calculate share of cumulative population for this scope
                world_cumulative_pop = base_df[
                    base_df['ISO2'] == 'WLD'
                ][f'Latest_cumulative_population_{scope}'].iloc[0]

                base_df[f'Share_of_cumulative_population_{scope}'] = base_df[f'Latest_cumulative_population_{scope}'] / world_cumulative_pop

            print("Base dataframe created successfully.")
            return base_df
        except Exception as e:
            print(f"Error creating base dataframe: {e}")
            return pd.DataFrame()
