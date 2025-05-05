import os
from utils.io import LoadData, DataAnalysis
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR")
DATABASE_URL = os.getenv("DATABASE_URL")

if not OUTPUT_DIR:
    raise ValueError("❌ ERROR: OUTPUT_DIR is not set. Please check your .env file.")

if not DATABASE_URL:
    raise ValueError("❌ ERROR: DATABASE_URL is not set. Please check your .env file.")
# File names
iso_code_map = os.getenv("iso_code_map")
iso_country_code = os.getenv("iso_country_code")
carbon_neutrality_timeline = os.getenv("carbon_neutrality_timeline")
gdp_ppp_constant = os.getenv("gdp_ppp_constant")
population_timeline = os.getenv("population_timeline")
co2_emission_territory = os.getenv("co2_emission_territory")
co2_emission_consumption = os.getenv("co2_emission_consumption")

iso_mapping = LoadData.load_iso_codes_mapping(DATA_DIR, iso_code_map)
ipcc_regions = LoadData.load_ipcc_regions(DATA_DIR, iso_country_code)
eu_g20_mapping = LoadData.load_eu_g20_mapping(DATA_DIR, iso_country_code)
historical_population_data = LoadData.load_historical_population_data(DATA_DIR, co2_emission_territory)
forecasted_population_data = LoadData.load_forecasted_population_data(DATA_DIR, population_timeline)
emissions_data = LoadData.load_emissions_data(DATA_DIR, co2_emission_territory)
consumption_emissions_data = LoadData.load_consumption_emissions_data(DATA_DIR, co2_emission_consumption)
# Define global carbon budgets
BUDGET_GLOBAL_lamboll_2C = {"33%": 1603000, "50%": 1219000, "67%": 944000}
BUDGET_GLOBAL_foster_2C = {"33%": 1450000, "50%": 1150000, "67%": 950000}
BUDGET_GLOBAL_lamboll_15C = {"33%": 480000, "50%": 247000, "67%": 60000}
BUDGET_GLOBAL_foster_15C = {"33%": 300000, "50%": 250000, "67%": 150000}