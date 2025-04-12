import numpy as np
from scipy import stats
import pandas as pd
from datetime import datetime


class MarketProbabilityAnalyzer:
    def __init__(self):
        # Base economic factors (hypothetical values)
        self.economic_factors = {
            "interest_rate": 0.0425,  # 4.25%
            "inflation_rate": 0.031,  # 3.1%
            "gdp_growth": 0.022,  # 2.2%
            "unemployment_rate": 0.036,  # 3.6%
        }

        # Social sentiment factors (scale -1 to 1)
        self.social_factors = {
            "market_sentiment": 0.3,
            "social_media_buzz": 0.4,
            "news_sentiment": 0.25,
        }

        # Market volatility (historical)
        self.volatility = {
            "stocks": 0.18,  # 18% annual volatility
            "crypto": 0.65,  # 65% annual volatility
        }

    def calculate_base_probability(self, asset_type="stocks"):
        """Calculate base probability of price movement"""
        # Weight economic factors
        econ_score = (
            self.economic_factors["gdp_growth"]
            - self.economic_factors["interest_rate"]
            - self.economic_factors["inflation_rate"]
            + (0.1 - self.economic_factors["unemployment_rate"])
        ) / 4

        # Weight social factors
        social_score = (
            self.social_factors["market_sentiment"]
            + self.social_factors["social_media_buzz"]
            + self.social_factors["news_sentiment"]
        ) / 3

        # Combine scores with volatility
        volatility = self.volatility[asset_type]
        base_prob = (econ_score + social_score) * volatility + 0.5

        return max(0.1, min(0.9, base_prob))  # Keep probability between 10% and 90%

    def simulate_price_movement(self, current_price, days=30, asset_type="stocks"):
        """Monte Carlo simulation of price movements"""
        n_simulations = 10000
        volatility = self.volatility[asset_type]
        base_prob = self.calculate_base_probability(asset_type)

        # Daily returns simulation
        daily_returns = np.random.normal(
            loc=base_prob / 252,  # Annual to daily return
            scale=volatility / np.sqrt(252),  # Annual to daily volatility
            size=(days, n_simulations),
        )

        # Calculate price paths
        price_paths = current_price * np.exp(np.cumsum(daily_returns, axis=0))

        return price_paths

    def calculate_drop_probability(
        self, current_price, threshold_percent, days=30, asset_type="stocks"
    ):
        """Calculate probability of price dropping below threshold"""
        price_paths = self.simulate_price_movement(current_price, days, asset_type)

        # Calculate final prices
        final_prices = price_paths[-1]

        # Calculate percentage drops
        drop_threshold = current_price * (1 - threshold_percent / 100)
        drops = final_prices < drop_threshold

        # Probability of drop
        drop_prob = np.mean(drops)

        return drop_prob, final_prices

    def analyze_market(self, stock_price=100, crypto_price=50000):
        """Analyze both stock and crypto markets"""
        thresholds = [5, 10, 20, 30]  # Percentage drop thresholds

        results = {"stocks": {}, "crypto": {}}

        for threshold in thresholds:
            # Stock analysis
            stock_prob, stock_prices = self.calculate_drop_probability(
                stock_price, threshold, asset_type="stocks"
            )
            results["stocks"][f"{threshold}%"] = {
                "drop_probability": stock_prob,
                "expected_price": np.mean(stock_prices),
            }

            # Crypto analysis
            crypto_prob, crypto_prices = self.calculate_drop_probability(
                crypto_price, threshold, asset_type="crypto"
            )
            results["crypto"][f"{threshold}%"] = {
                "drop_probability": crypto_prob,
                "expected_price": np.mean(crypto_prices),
            }

        return results


# Example usage
def main():
    analyzer = MarketProbabilityAnalyzer()

    # Analyze markets with sample prices
    results = analyzer.analyze_market(
        stock_price=100,  # Sample stock price (e.g., index value)
        crypto_price=50000,  # Sample crypto price (e.g., Bitcoin)
    )

    # Print results
    print(f"Market Analysis - Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("\nStock Market Probabilities:")
    for threshold, data in results["stocks"].items():
        print(f"Probability of {threshold} drop: {data['drop_probability']:.2%}")
        print(f"Expected price after 30 days: ${data['expected_price']:.2f}")

    print("\nCrypto Market Probabilities:")
    for threshold, data in results["crypto"].items():
        print(f"Probability of {threshold} drop: {data['drop_probability']:.2%}")
        print(f"Expected price after 30 days: ${data['expected_price']:.2f}")


if __name__ == "__main__":
    main()
