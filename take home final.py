import os
import json
from pathlib import Path
import logging
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('currency_analysis.log'),
        logging.StreamHandler()
    ]
)


class CurrencyDataAnalyzer:
    def __init__(self, base_currency):
        #Set up the analyzer with the given base currency.
        self.base_currency = base_currency
        self.data_path = Path(f"currency_data/{base_currency}")

        if not self.data_path.exists(): #error handling if missing data
            logging.error(f"Data folder not found for {base_currency}")
            raise FileNotFoundError(f"Directory does not exist: {self.data_path}")
        
        logging.info(f"Analyzer initialized for base currency: {base_currency}")
        self.df = None

    def load_data(self):
        #Load all JSON files and compile into a single DataFrame.
        records = []
        files = list(self.data_path.glob("*_exchange_rates.json"))

        if not files:
            logging.error("No JSON data files found.")
            return False

        logging.info(f"Found {len(files)} JSON files.")

        for file in files:
            try:
                date_str = file.name.split("_")[0]
                date = datetime.strptime(date_str, "%Y-%m-%d")

                with open(file, "r") as f:
                    data = json.load(f)

                items = data.get("channel", {}).get("item", [])
                if isinstance(items, dict):
                    items = [items]

                for item in items:
                    code = item.get("targetCurrency", {}).get("targetCurrencyCode")
                    rate = item.get("exchangeRate", {}).get("rateNew", 0)

                    if code:
                        records.append({
                            "date": date,
                            "currency": code,
                            "rate": float(rate)
                        })

            except Exception as e:
                logging.warning(f"Failed to load {file.name}: {e}")

        if records:
            self.df = pd.DataFrame(records)
            self.df["date"] = pd.to_datetime(self.df["date"])
            logging.info("Data loaded successfully.")
            return True
        else:
            logging.error("No valid data")
            return False

    def prepare_data(self): #assisted by copilot
        #Clean and reshape data for analysis.
        if self.df is None:
            logging.error("No data")
            return False

        try:
            pivot = self.df.pivot(index="date", columns="currency", values="rate")
            pivot = pivot.sort_index().fillna(method="ffill")
            self.pivoted_df = pivot
            logging.info("Data reshaped and cleaned.")
            return True
        except Exception as e:
            logging.error(f"Error during data prep: {e}")
            return False

    def analyze_volatility(self, currencies=None):
        #find volatility stats for selected currencies.
        if not hasattr(self, "pivoted_df"):
            logging.error("Data not prepared. Run prepare_data() first.")
            return None

        if currencies is None:
            major = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
            currencies = [c for c in major if c in self.pivoted_df.columns]
            if not currencies:
                currencies = self.pivoted_df.columns[:5].tolist()

        data = self.pivoted_df[currencies]
        changes = data.pct_change().dropna()
        volatility = changes.std()

        stats = pd.DataFrame({
            "volatility": volatility,
            "min_rate": data.min(),
            "max_rate": data.max(),
            "max_daily_change": changes.abs().max(),
            "mean_rate": data.mean()
        })

        logging.info("Volatility stats calculated.")
        return stats

    def plot_exchange_rates(self, currencies=None, start_date=None, end_date=None):

        #Plot exchange rates for selected currencies #(syntax assisted by copilot)
        if not hasattr(self, "pivoted_df"):
            logging.error("Data not ready. Use prepare_data() first.")
            return None

        if currencies is None:
            major = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
            currencies = [c for c in major if c in self.pivoted_df.columns]
            if not currencies:
                currencies = self.pivoted_df.columns[:5].tolist()

        data = self.pivoted_df[currencies]

        if start_date:
            data = data[data.index >= pd.to_datetime(start_date)]
        if end_date:
            data = data[data.index <= pd.to_datetime(end_date)]

        plt.figure(figsize=(12, 8))
        sns.lineplot(data=data)
        plt.title(f"Exchange Rates vs {self.base_currency}")
        plt.xlabel("Date")
        plt.ylabel(f"Rate (per {self.base_currency})")
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.legend(title="Currency")
        logging.info("Exchange rate plot created.")
        return plt.gcf()

    def plot_volatility_heatmap(self, window=30):
        #Heatmap of rolling volatility.
        if not hasattr(self, "pivoted_df"):
            logging.error("Data not ready. Use prepare_data() first.")
            return None

        major = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
        currencies = [c for c in major if c in self.pivoted_df.columns]
        if not currencies:
            currencies = self.pivoted_df.columns[:5].tolist()

        rolling_vol = self.pivoted_df[currencies].pct_change().rolling(window=window).std()
        monthly = rolling_vol.resample("M").mean()

        plt.figure(figsize=(14, 10))
        sns.heatmap(monthly.T, cmap="YlOrRd", robust=True)
        plt.title(f"{window}-Day Rolling Volatility")
        plt.ylabel("Currency")
        plt.xlabel("Date")
        logging.info("Volatility heatmap created.")
        return plt.gcf()

    def plot_correlation_matrix(self):
        #Heatmap of correlation matrix between currencies 
        if not hasattr(self, "pivoted_df"):
            logging.error("Data not ready. Use prepare_data() first.")
            return None

        major = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
        currencies = [c for c in major if c in self.pivoted_df.columns]

        if len(currencies) < 5:
            extra = [c for c in self.pivoted_df.columns if c not in currencies]
            currencies += extra[:5 - len(currencies)]

        corr = self.pivoted_df[currencies].pct_change().corr()

        plt.figure(figsize=(10, 8)) #copilot helped with the syntax again
        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Currency Movement Correlation")
        plt.tight_layout()
        logging.info("Correlation matrix plotted.")
        return plt.gcf()

    def identify_extreme_periods(self, currencies=None, percentile=95):
        #Identify unusually volatile days for selected currencies
        if not hasattr(self, "pivoted_df"):
            logging.error("Data not ready. Use prepare_data() first.")
            return None

        if currencies is None:
            major = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
            currencies = [c for c in major if c in self.pivoted_df.columns]
            if not currencies:
                currencies = self.pivoted_df.columns[:5].tolist()

        changes = self.pivoted_df[currencies].pct_change().abs()
        thresholds = changes.quantile(percentile / 100)

        result = {}
        for c in currencies:
            extreme_dates = changes[changes[c] > thresholds[c]].index.tolist()
            result[c] = extreme_dates

        logging.info("Extreme volatility periods ided.")
        return result


def main():
    base_currency = "AUD"  #example 
    try:
        analyzer = CurrencyDataAnalyzer(base_currency)

        if analyzer.load_data() and analyzer.prepare_data():
            metrics = analyzer.analyze_volatility()
            print("\nVolatility Metrics:\n", metrics)

            plt.figure(1)
            analyzer.plot_exchange_rates()
            plt.tight_layout()
            plt.savefig(f"{base_currency}_exchange_rates.png")

            plt.figure(2)
            analyzer.plot_volatility_heatmap()
            plt.tight_layout()
            plt.savefig(f"{base_currency}_volatility_heatmap.png")

            plt.figure(3)
            analyzer.plot_correlation_matrix()
            plt.tight_layout()
            plt.savefig(f"{base_currency}_correlation_matrix.png")

            extremes = analyzer.identify_extreme_periods() #plot was made with assistance from copilot
            print("\nExtreme Volatility Periods:")
            for currency, days in extremes.items():
                if days:
                    print(f"{currency}: {len(days)} extreme days")
                    sample = [d.strftime("%Y-%m-%d") for d in days[:5]] 
                    print(f"Sample: {', '.join(sample)}")

        else:
            logging.error("error lmao try again")

    except Exception as e:
        logging.error(f"Something went wrong in main(): {e}")


if __name__ == "__main__":
    main()

#I hope you could have mercy on me.