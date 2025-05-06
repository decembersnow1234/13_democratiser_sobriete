class ForecastProcessor:
    """Handles scenario forecasting."""

    @staticmethod
    def generate_forecast(scenario_params):
        """Generate forecast data based on scenarios."""
        forecast_data = []
        for _, row in scenario_params.iterrows():
            if pd.isna(row["Latest_year"]) or pd.isna(row["Latest_annual_CO2_emissions_Mt"]):
                continue

            latest_year = int(row["Latest_year"])
            neutrality_year = int(row["Neutrality_year"]) if row["Neutrality_year"].isdigit() else 2100

            forecast_years = pd.DataFrame({"Year": range(latest_year + 1, neutrality_year + 1)})
            slope = -row["Latest_annual_CO2_emissions_Mt"] / (neutrality_year - latest_year)

            forecast_years["Forecasted_emissions_Mt"] = [
                max(0, row["Latest_annual_CO2_emissions_Mt"] + slope * (year - latest_year))
                for year in forecast_years["Year"]
            ]

            for _, year_row in forecast_years.iterrows():
                forecast_data.append({
                    "scenario_id": row["scenario_id"],
                    "Year": year_row["Year"],
                    "Forecasted_emissions_Mt": year_row["Forecasted_emissions_Mt"]
                })

        return pd.DataFrame(forecast_data)
