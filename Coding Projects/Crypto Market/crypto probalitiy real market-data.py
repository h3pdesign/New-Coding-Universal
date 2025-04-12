import numpy as np
import pandas as pd

# Define parameters
S0_btc = 77254.87  # Current price of Bitcoin ($)
sigma_btc = 0.0891  # Annualized volatility of Bitcoin (8.91%)
S0_eth = 1457.66  # Current price of Ethereum ($)
sigma_eth = 0.1324  # Annualized volatility of Ethereum (13.24%)
mu = 0.05  # Annualized drift (5%)
N = 10000  # Number of simulation paths
dt = 1 / 252  # Time step (1 trading day, assuming 252 trading days per year)
horizons = [2, 5, 10, 14, 30]  # Time horizons in days


# Function to simulate price paths using geometric Brownian motion
def simulate_prices(S0, sigma, mu, dt, N, max_days):
    """
    Simulate future price paths using Monte Carlo simulation.

    Parameters:
    - S0: Initial price
    - sigma: Annualized volatility
    - mu: Annualized drift
    - dt: Time step (fraction of a year)
    - N: Number of simulation paths
    - max_days: Maximum number of days to simulate

    Returns:
    - prices: Array of simulated prices (days x simulations)
    """
    # Generate daily increments
    increments = np.random.normal(
        loc=(mu - 0.5 * sigma**2) * dt, scale=sigma * np.sqrt(dt), size=(max_days, N)
    )
    # Cumulative sum of log returns
    log_returns = np.cumsum(increments, axis=0)
    # Convert to price paths
    prices = S0 * np.exp(log_returns)
    return prices


# Run simulations for Bitcoin and Ethereum
prices_btc = simulate_prices(S0_btc, sigma_btc, mu, dt, N, 30)
prices_eth = simulate_prices(S0_eth, sigma_eth, mu, dt, N, 30)

# Collect results in a dictionary
results = {}
results["Current Price ($)"] = [f"{S0_btc:,.2f}", f"{S0_eth:,.2f}"]
results["Volatility"] = [f"{sigma_btc:.2%}", f"{sigma_eth:.2%}"]

# Calculate metrics for each time horizon
for d in horizons:
    # Bitcoin metrics
    prob_down_btc = np.mean(
        prices_btc[d - 1, :] < S0_btc
    )  # Probability price decreases
    prob_up_btc = np.mean(prices_btc[d - 1, :] > S0_btc)  # Probability price increases
    expected_price_btc = np.mean(prices_btc[d - 1, :])  # Average simulated price

    # Ethereum metrics
    prob_down_eth = np.mean(prices_eth[d - 1, :] < S0_eth)
    prob_up_eth = np.mean(prices_eth[d - 1, :] > S0_eth)
    expected_price_eth = np.mean(prices_eth[d - 1, :])

    # Store formatted results
    results[f"Prob Down at {d} days"] = [f"{prob_down_btc:.2%}", f"{prob_down_eth:.2%}"]
    results[f"Prob Up at {d} days"] = [f"{prob_up_btc:.2%}", f"{prob_up_eth:.2%}"]
    results[f"Expected Price at {d} days"] = [
        f"{expected_price_btc:,.2f}",
        f"{expected_price_eth:,.2f}",
    ]

# Create DataFrame with metrics as rows and cryptocurrencies as columns
df = pd.DataFrame(results, index=["Bitcoin", "Ethereum"]).T

# Print the analysis table
print("Market Analysis - Date: 2025-04-09")
print(df.to_string())
