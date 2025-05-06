import pandas as pd
from utils.io import LoadData, DataAnalysis
from config.carbon_budget import BUDGET_GLOBAL  # Centralized carbon budget data

class ScenarioGenerator:
    """Generates forecast scenarios for climate targets."""

    def __init__(self, base_df, current_targets):
        """Initialize scenario generator with base data and targets."""
        self.base_df = base_df
        self.current_targets = current_targets
        self.scenarios = []

    def calculate_country_budget(self, row, emissions_scope, warming_scenario, probability, budget_source, distribution):
        """Calculate the carbon budget for a country based on distribution scenario."""
        global_budget = BUDGET_GLOBAL[f"{budget_source.lower()}_{warming_scenario.replace('°', '')}C"][probability]

        if distribution == "Equality":
            return global_budget * row["Share_of_total_population_2050"]

        elif distribution == "Responsibility":
            world_cumulative = self.base_df[
                (self.base_df["ISO2"] == "WLD") &
                (self.base_df[f"Latest_cumulative_CO2_emissions_Mt_{emissions_scope}"].notna())
            ][f"Latest_cumulative_CO2_emissions_Mt_{emissions_scope}"].iloc[0]

            total_available = global_budget + world_cumulative
            country_cumulative = row[f"Latest_cumulative_CO2_emissions_Mt_{emissions_scope}"]

            return (total_available * row[f"Share_of_cumulative_population_{emissions_scope}"]) - country_cumulative

        elif distribution == "Current_target":
            return None  # Handled in another method
        else:
            raise ValueError("Invalid distribution type")

    def generate_scenarios(self):
        """Generate all ETL scenarios."""
        for _, row in self.base_df.iterrows():
            for emissions_scope in ["Territory", "Consumption"]:
                for warming_scenario in ["1.5°C", "2°C"]:
                    for probability in ["33%", "50%", "67%"]:
                        for budget_source in ["Lamboll", "Foster"]:
                            for distribution in ["Equality", "Responsibility", "Current_target"]:
                                country_budget = self.calculate_country_budget(
                                    row, emissions_scope, warming_scenario, probability, budget_source, distribution
                                )

                                # Determine neutrality year
                                neutrality_year, years_to_neutrality = self.calculate_neutrality_year(row, emissions_scope, distribution, country_budget)

                                self.scenarios.append(self.create_scenario_dict(row, emissions_scope, warming_scenario, probability, budget_source, distribution, country_budget, neutrality_year, years_to_neutrality))

        return pd.DataFrame(self.scenarios)

    def calculate_neutrality_year(self, row, emissions_scope, distribution, country_budget):
        """Calculate the neutrality year for a country based on scenario."""
        latest_annual = row[f"Latest_annual_CO2_emissions_Mt_{emissions_scope}"]
        latest_year = row[f"Latest_year_{emissions_scope}"]

        if distribution == "Current_target":
            neutrality_year = self.current_targets.get(row["ISO2"], "N/A")
            if neutrality_year != "N/A":
                years_to_neutrality = neutrality_year - latest_year
                if pd.notna(latest_annual) and latest_annual > 0:
                    country_budget = (years_to_neutrality * latest_annual) / 2
            else:
                years_to_neutrality = "N/A"
        elif pd.notna(country_budget) and pd.notna(latest_annual) and latest_annual > 0:
            years_to_neutrality = int(round(2 * country_budget / latest_annual))
            neutrality_year = self.adjust_neutrality_year(years_to_neutrality, latest_year)
        else:
            years_to_neutrality, neutrality_year = "N/A", "N/A"

        return neutrality_year, years_to_neutrality

    @staticmethod
    def adjust_neutrality_year(years_to_neutrality, latest_year):
        """Adjust neutrality year based on constraints."""
        if years_to_neutrality + latest_year > 2100:
            return ">2100"
        elif years_to_neutrality + latest_year < 2023:
            return "<2023"
        else:
            return int(round(latest_year + years_to_neutrality))

    def create_scenario_dict(self, row, emissions_scope, warming_scenario, probability, budget_source, distribution, country_budget, neutrality_year, years_to_neutrality):
        """Create a dictionary representing a scenario."""
        return {
            "ISO2": row["ISO2"],
            "Country": row["Country"],
            "Region": row["Region"],
            "Population_2050": row["Population_2050"],
            "Share_of_total_population_2050": row["Share_of_total_population_2050"],
            "Emissions_scope": emissions_scope,
            "Latest_year": row[f"Latest_year_{emissions_scope}"],
            "Latest_annual_CO2_emissions_Mt": row[f"Latest_annual_CO2_emissions_Mt_{emissions_scope}"],
            "Latest_cumulative_CO2_emissions_Mt": row[f"Latest_cumulative_CO2_emissions_Mt_{emissions_scope}"],
            "Latest_cumulative_population": row[f"Latest_cumulative_population_{emissions_scope}"],
            "Share_of_cumulative_population": row[f"Share_of_cumulative_population_{emissions_scope}"],
            "Warming_scenario": warming_scenario,
            "Probability_of_reach": probability,
            "Budget_source": budget_source,
            "Budget_distribution_scenario": distribution,
            "Global_Carbon_budget": BUDGET_GLOBAL[f"{budget_source.lower()}_{warming_scenario.replace('°', '')}C"][probability],
            "Country_carbon_budget": country_budget,
            "Years_to_neutrality": years_to_neutrality,
            "Neutrality_year": neutrality_year
        }
