import pandas as pd
from config import paths
from dotenv import load_dotenv
import os
load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR")
DATABASE_URL = os.getenv("DATABASE_URL")

class LoadData:
    @staticmethod
    def get_file_path(file_name):
        return os.path.join(OUTPUT_DIR, file_name)

    @staticmethod
    def read_csv(file_name):
        path = LoadData.get_file_path(file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        if os.path.getsize(path) == 0:
            raise ValueError(f"❌ File is empty: {path}")
        return pd.read_csv(path, low_memory=False)
    @staticmethod
    def load_iso_codes_mapping(DATA_DIR, iso_code_map):
        """Load and process ISO codes mapping data."""
        print("Loading ISO codes mapping data...")
        iso_mapping = pd.read_excel(f"{DATA_DIR}/{iso_code_map}")
        iso_mapping.rename(columns={'Alpha-2 code': 'ISO2', 'Alpha-3 code': 'ISO3'}, inplace=True)
        iso_mapping['ISO2'] = iso_mapping['ISO2'].fillna('')
        return iso_mapping[['ISO3', 'ISO2']]

    @staticmethod
    def load_ipcc_regions(DATA_DIR, iso_country_code):
        """Load and process IPCC region mapping data."""
        print("Loading IPCC region mapping data...")
        regions = pd.read_excel(os.path.join(settings.DATA_DIR,iso_country_code), sheet_name="Full_mapping")
        regions = regions[['Intermediate level (10)', 'ISO codes']]
        regions.rename(columns={'Intermediate level (10)': 'IPCC_Region_Intermediate', 'ISO codes': 'ISO3'}, inplace=True)
        expanded_regions = []
        for _, row in regions.iterrows():
            for iso in row['ISO3'].split(','):
                expanded_regions.append({
                    'IPCC_Region_Intermediate': row['IPCC_Region_Intermediate'],
                    'ISO3': iso.strip()
                })
        return pd.DataFrame(expanded_regions)

    @staticmethod
    def load_eu_g20_mapping(DATA_DIR, iso_country_code):
        """Load EU and G20 country mappings."""
        print("Loading EU and G20 country mappings...")
        mapping = pd.read_excel(os.path.join(DATA_DIR,iso_country_code), sheet_name="G20_EU_Countries ", header=0)
        return mapping[['ISO3', 'EU_country', 'G20_country']]

    @staticmethod
    def load_historical_population_data(DATA_DIR, co2_emission_territory):
        """Load and process historical population data from emissions data."""
        print("Loading historical population data...")
        emissions = pd.read_excel(os.path.join(DATA_DIR,co2_emission_territory), sheet_name="GCB2024v17_MtCO2_flat")
        emissions = emissions[['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total', 'Per Capita']]
        emissions.rename(columns={
            'ISO 3166-1 alpha-3': 'ISO3',
            'Per Capita': 'Per_Capita',
            'Total': 'Annual_CO2_emissions_Mt'
        }, inplace=True)
        emissions['Population'] = round(((emissions['Annual_CO2_emissions_Mt'] / emissions['Per_Capita']) * 1000000), 0)
        return emissions[['ISO3', 'Country', 'Year', 'Population']]

    @staticmethod
    def load_forecasted_population_data(DATA_DIR, population_timeline):
        """Load and process forecasted population data for 2050."""
        print("Loading forecasted population data...")
        pop = pd.read_excel(os.path.join(DATA_DIR,population_timeline), sheet_name="unpopulation_dataportal_2025042")
        pop = pop[['Iso3', 'Location', 'Time', 'Value']]
        pop.rename(columns={'Iso3': 'ISO3', 'Location': 'Country', 'Time': 'Year', 'Value': 'Population'}, inplace=True)
        return pop[pop['Year'] == 2050]

    @staticmethod
    def load_emissions_data(DATA_DIR, co2_emission_territory):
        """Load and process CO2 emissions data."""
        print("Loading CO2 emissions data...")
        emissions = pd.read_excel(os.path.join(DATA_DIR,co2_emission_territory), sheet_name="GCB2024v17_MtCO2_flat")
        emissions = emissions[['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total']]
        emissions.rename(columns={'ISO 3166-1 alpha-3': 'ISO3', 'Total': 'Annual_CO2_emissions_Mt'}, inplace=True)
        return emissions

    @staticmethod
    def load_consumption_emissions_data(DATA_DIR, co2_emission_consumption):
        """Load and process consumption emissions data."""
        print("Loading consumption emissions data...")
        cons_emissions = pd.read_excel(os.path.join(DATA_DIR,co2_emission_consumption), sheet_name="GCB2024v17_MtCO2_flat")
        cons_emissions = cons_emissions[['Country', 'ISO 3166-1 alpha-3', 'Year', 'CO2_Consumption_emissions in Mt']]
        cons_emissions.rename(columns={
            'ISO 3166-1 alpha-3': 'ISO3',
            'CO2_Consumption_emissions in Mt': 'Annual_CO2_emissions_Mt'
        }, inplace=True)
        cons_emissions['Annual_CO2_emissions_Mt'] = cons_emissions['Annual_CO2_emissions_Mt'].apply(
            lambda x: float(str(x).replace(',', '.')) if isinstance(x, str) else float(x)
        ).round(2)
        return cons_emissions