import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range: Last 14 days ending April 9, 2025
end_date = datetime(2025, 4, 9)
start_date = end_date - timedelta(days=13)  # 14 days total, inclusive


def fetch_historical_data(ticker, start, end):
    """Fetch historical data from Yahoo Finance."""
    try:
        data = yf.download(ticker, start=start, end=end + timedelta(days=1))
        if data.empty:
            raise ValueError(f"No data returned for {ticker}")
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def calculate_metrics(data, asset_name):
    """Calculate market metrics from historical data."""
    if data is None or len(data) < 2:
        print(f"Insufficient data for {asset_name} analysis")
        return {
            "Current Price ($)": "N/A",
            "Average Daily Return (%)": "N/A",
            "Volatility (% per annum)": "N/A",
        }

    # Current price (last closing price) - ensure scalar value
    current_price = data["Close"].iloc[-1]
    if isinstance(current_price, pd.Series):
        current_price = current_price.item()  # Extract scalar value from Series

    # Daily returns - ensure it's a scalar series
    daily_returns = data["Close"].pct_change().dropna()
    if isinstance(daily_returns, pd.Series) and daily_returns.size > 0:
        # Average daily return (as percentage)
        avg_daily_return = daily_returns.mean() * 100
        if isinstance(avg_daily_return, pd.Series):
            avg_daily_return = avg_daily_return.item()  # Ensure scalar

        # Annualized volatility (as percentage)
        daily_volatility = daily_returns.std()
        if isinstance(daily_volatility, pd.Series):
            daily_volatility = daily_volatility.item()  # Ensure scalar
        annualized_volatility = (
            daily_volatility * np.sqrt(252) * 100
        )  # 252 trading days
    else:
        print(f"Failed to compute returns for {asset_name}")
        return {
            "Current Price ($)": f"{current_price:,.2f}",
            "Average Daily Return (%)": "N/A",
            "Volatility (% per annum)": "N/A",
        }

    return {
        "Current Price ($)": f"{current_price:,.2f}",
        "Average Daily Return (%)": f"{avg_daily_return:.2f}",
        "Volatility (% per annum)": f"{annualized_volatility:.2f}",
    }


def main():
    # Fetch data for S&P 500 and Bitcoin
    sp500_data = fetch_historical_data("^GSPC", start_date, end_date)
    bitcoin_data = fetch_historical_data("BTC-USD", start_date, end_date)

    # Calculate metrics
    sp500_metrics = calculate_metrics(sp500_data, "S&P 500")
    bitcoin_metrics = calculate_metrics(bitcoin_data, "Bitcoin")

    # Create DataFrame for table
    metrics_df = pd.DataFrame(
        {
            "Metric": [
                "Current Price ($)",
                "Average Daily Return (%)",
                "Volatility (% per annum)",
            ],
            "S&P 500": [
                sp500_metrics["Current Price ($)"],
                sp500_metrics["Average Daily Return (%)"],
                sp500_metrics["Volatility (% per annum)"],
            ],
            "Bitcoin": [
                bitcoin_metrics["Current Price ($)"],
                bitcoin_metrics["Average Daily Return (%)"],
                bitcoin_metrics["Volatility (% per annum)"],
            ],
        }
    ).set_index("Metric")

    # Print the analysis table
    print(f"Market Analysis - Date: {end_date.strftime('%Y-%m-%d')}")
    print(metrics_df.to_string())

    # Optional: Print raw historical data for verification
    if sp500_data is not None:
        print("\nS&P 500 Historical Data (Last 5 Days):")
        print(sp500_data[["Close"]].tail().to_string())
    if bitcoin_data is not None:
        print("\nBitcoin Historical Data (Last 5 Days):")
        print(bitcoin_data[["Close"]].tail().to_string())


if __name__ == "__main__":
    # Ensure required library is installed
    try:
        import yfinance
    except ImportError:
        print("Please install yfinance: `pip install yfinance`")
        exit(1)

    main()
