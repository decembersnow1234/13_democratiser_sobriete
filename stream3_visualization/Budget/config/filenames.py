from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"

# File paths
FILES = {
    "iso_country_code": {
        "path": DATA_DIR / "2024-04-21_IPCC Regional Breakdown_ISO Country Code.xlsx",
        "sheet": "Full_mapping"
    },
    "carbon_neutrality_timeline": {
        "path": DATA_DIR / "2025-04-21_Full file_Current carbon neutrality timeline per with Country ISO code.xlsx",
        "sheet": "Neutrality_Timeline"
    },
    "gdp_ppp_constant": {
        "path": DATA_DIR / "2025-04-21_GDP _PPP constant 2021 US$_per country ISO Code.xlsx",
        "sheet": "GDP_PPP"
    },
    "population_timeline": {
        "path": DATA_DIR / "2025-04-21_Population per Country ISO code_1970-2050.xlsx",
        "sheet": "Population"
    },
    "co2_emission_territory": {
        "path": DATA_DIR / "2025-04-22_CO2 Emissions_All Countries_ISO Code_1750-2023.xlsx",
        "sheet": "GCB2024v17_MtCO2_flat"
    },
    "co2_emission_consumption": {
        "path": DATA_DIR / "2025-04-22_Consumption emissions MtCO2_ISO code.xlsx",
        "sheet": "Consumption_Emissions"
    }
}


"""
iso_country_code = DATA_DIR / "2024-04-21_IPCC Regional Breakdown_ISO Country Code.xlsx"
carbon_neutrality_timeline = DATA_DIR / "2025-04-21_Full file_Current carbon neutrality timeline per with Country ISO code.xlsx"
gdp_ppp_constant = DATA_DIR / "2025-04-21_GDP _PPP constant 2021 US$_per country ISO Code.xlsx"
population_timeline = DATA_DIR / "2025-04-21_Population per Country ISO code_1970-2050.xlsx"
co2_emission_territory = DATA_DIR / "2025-04-22_CO2 Emissions_All Countries_ISO Code_1750-2023.xlsx"
co2_emission_consumption = DATA_DIR / "2025-04-22_Consumption emissions MtCO2_ISO code.xlsx"
"""