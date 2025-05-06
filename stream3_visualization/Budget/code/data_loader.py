import sys
import os

# Add the parent directory to the path (using raw string for the file path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'..')))

import pandas as pd
from config import filenames

from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR")
DATABASE_URL = os.getenv("DATABASE_URL")

from file_handler import FileHandler
class DataLoader:
    @staticmethod
    def __init__(self, iso_codes_file, population_file, emissions_file):
        self.iso_codes_file = iso_codes_file
        self.population_file = population_file
        self.emissions_file = emissions_file
    
    def load_iso_codes(self):
        print("Loading ISO codes mapping...")
        return FileHandler.read_excel(self.iso_codes_file)

    def load_population_data(self):
        print("Loading Population data...")
        return FileHandler.read_csv(self.population_file)

    def load_emissions_data(self):
        print("Loading Emissions data...")
        return FileHandler.read_csv(self.emissions_file)
    
  #  starting from here: LTL's code

    def load_iso_codes_mapping(file_name):
        """Load and process ISO codes mapping data."""
        print("Loading ISO codes mapping data...")
        iso_mapping = pd.read_excel(file_name)
        iso_mapping.rename(columns={'Alpha-2 code': 'ISO2', 'Alpha-3 code': 'ISO3'}, inplace=True)
        iso_mapping['ISO2'] = iso_mapping['ISO2'].fillna('')  # Fill NaN values with empty strings
        return iso_mapping[['ISO3', 'ISO2']]
    
    @staticmethod
    def load_ipcc_regions(file_name):
        """Load and process IPCC region mapping data."""
        print("Loading IPCC region mapping data...")
        regions = pd.read_excel(file_name, sheet_name="Full_mapping")
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
    def load_eu_g20_mapping(file_name):
        """Load EU and G20 country mappings."""
        print("Loading EU and G20 country mappings...")
        mapping = pd.read_excel(file_name, sheet_name="G20_EU_Countries ", header=0)
        return mapping[['ISO3', 'EU_country', 'G20_country']]

    @staticmethod
    def load_historical_population_data(file_name):
        """Load and process historical population data from emissions data."""
        print("Loading historical population data...")
        emissions = pd.read_excel(file_name, sheet_name="GCB2024v17_MtCO2_flat")
        emissions = emissions[['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total', 'Per Capita']]
        emissions.rename(columns={
            'ISO 3166-1 alpha-3': 'ISO3',
            'Per Capita': 'Per_Capita',
            'Total': 'Annual_CO2_emissions_Mt'
        }, inplace=True)
        emissions['Population'] = round(((emissions['Annual_CO2_emissions_Mt'] / emissions['Per_Capita']) * 1000000), 0)
        return emissions[['ISO3', 'Country', 'Year', 'Population']]

    @staticmethod
    def load_forecasted_population_data(file_name):
        """Load and process forecasted population data for 2050."""
        print("Loading forecasted population data...")
        pop = pd.read_excel(file_name, sheet_name="unpopulation_dataportal_2025042")
        pop = pop[['Iso3', 'Location', 'Time', 'Value']]
        pop.rename(columns={'Iso3': 'ISO3', 'Location': 'Country', 'Time': 'Year', 'Value': 'Population'}, inplace=True)
        return pop[pop['Year'] == 2050]

    @staticmethod
    def load_emissions_data(file_name):
        """Load and process CO2 emissions data."""
        print("Loading CO2 emissions data...")
        emissions = pd.read_excel(file_name, sheet_name="GCB2024v17_MtCO2_flat")
        emissions = emissions[['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total']]
        emissions.rename(columns={'ISO 3166-1 alpha-3': 'ISO3', 'Total': 'Annual_CO2_emissions_Mt'}, inplace=True)
        return emissions

    @staticmethod
    def load_consumption_emissions_data(file_name):
        """Load and process consumption emissions data."""
        print("Loading consumption emissions data...")
