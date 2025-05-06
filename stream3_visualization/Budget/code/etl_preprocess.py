import pandas as pd
from data_loader import DataLoader
from file_handler import FileHandler
from config import ISO_CODES_FILE, POPULATION_FILE, EMISSIONS_FILE

class ETLProcessor:
    """Handles ETL preprocessing of emissions and population data."""

    def __init__(self):
        """Initialize data loader dynamically."""
        self.loader = DataLoader(ISO_CODES_FILE, POPULATION_FILE, EMISSIONS_FILE)
    
    def preprocess(self):
        """Run ETL preprocessing pipeline."""
        print("🔄 Running ETL Preprocessing...")
        
        iso_mapping = self.loader.load_iso_codes()
        population_data = self.loader.load_population_data()
        emissions_data = self.loader.load_emissions_data()

        # Create mappings from ISO codes
        iso2_mapping = iso_mapping.set_index('ISO3')['ISO2'].to_dict()
        population_data['ISO2'] = population_data['ISO3'].map(iso2_mapping)
        emissions_data['ISO2'] = emissions_data['ISO3'].map(iso2_mapping)

        # Process emissions data
        emissions_data['Emissions_per_capita'] = emissions_data['Annual_CO2_emissions_Mt'] * 1e6 / emissions_data['Population']

        # Save processed data
        FileHandler.save_csv(emissions_data, "processed_emissions.csv")

        return emissions_data
