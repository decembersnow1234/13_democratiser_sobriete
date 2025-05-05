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
# Define global carbon budgets
BUDGET_GLOBAL_lamboll_2C = {"33%": 1603000, "50%": 1219000, "67%": 944000}
BUDGET_GLOBAL_foster_2C = {"33%": 1450000, "50%": 1150000, "67%": 950000}
BUDGET_GLOBAL_lamboll_15C = {"33%": 480000, "50%": 247000, "67%": 60000}
BUDGET_GLOBAL_foster_15C = {"33%": 300000, "50%": 250000, "67%": 150000}