import pandas as pd
from file_handler import read_csv, save_csv

class VisualizationDataProcessor:
    """Handles merging historical and forecasted emissions data for visualization."""

    def __init__(self, combined_data, forecast_data, parameters):
        """
        Initialize processor with required datasets.
        
        :param combined_data: DataFrame containing historical emissions data.
        :param forecast_data: DataFrame containing forecast emissions data.
        :param parameters: DataFrame containing forecast scenario parameters.
        """
        self.combined_data = combined_data
        self.forecast_data = forecast_data
        self.parameters = parameters

    def enrich_forecast(self):
        """Modify forecast data structure and prepare for merging."""
        self.forecast_data["Annual_CO2_emissions_Mt"] = self.forecast_data["Forecasted_emissions_Mt"]
        self.forecast_data.drop(columns=["Forecasted_emissions_Mt"], inplace=True)

    def prepare_historical_data(self):
        """Extract relevant historical data for visualization."""
        self.history_df = self.combined_data[[
            "Country", "ISO2", "Region", "Sector", "Scope", "Year",
            "Annual_CO2_emissions_Mt", "Emissions_per_capita_ton", "Cumulative_CO2_emissions_Mt"
        ]]

    def merge_forecast_with_parameters(self):
        """Merge forecast data with scenario parameters."""
        self.merged_forecast = self.forecast_data.merge(self.parameters, on="scenario_id", how="left")

    def standardize_column_names(self):
        """Ensure consistent column names for merging."""
        self.merged_forecast.rename(columns={"Scope": "Emissions_scope"}, inplace=True)
        self.history_df.rename(columns={"Scope": "Emissions_scope"}, inplace=True)

    def merge_data(self):
        """Concatenate historical and forecast data."""
        final_df = pd.concat([self.history_df, self.merged_forecast], ignore_index=True, sort=False)
        final_df.sort_values(by=["ISO2", "Year"], inplace=True)
        final_df.reset_index(drop=True, inplace=True)
        return final_df

    def process(self):
        """Run all data transformations and save final merged dataset."""
        self.enrich_forecast()
        self.prepare_historical_data()
        self.merge_forecast_with_parameters()
        self.standardize_column_names()
        final_df = self.merge_data()

        save_csv(final_df, "viz_history_forecast_data.csv")
        return final_df
