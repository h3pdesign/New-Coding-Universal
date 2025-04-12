import random
import string
from datetime import datetime, timedelta
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(
    filename="crypto_wallets.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX")
NUM_WALLETS = int(os.getenv("NUM_WALLETS"))


# Function to generate a random Ethereum wallet address
def generate_wallet_address():
    return "0x" + "".join(random.choices(string.hexdigits.lower(), k=40))


# Function to generate a random time delta in a human-readable format
def generate_time_delta(min_hours, max_hours):
    hours = random.randint(min_hours, max_hours)
    minutes = random.randint(0, 59)
    return f"{hours}h {minutes}m"


# Function to generate a random "last activity" time
def generate_last_activity():
    hours_ago = random.randint(1, 48)
    if hours_ago < 24:
        return f"{hours_ago}h ago"
    else:
        days_ago = hours_ago // 24
        return f"{days_ago}d ago"


# Function to generate mock wallet data
def generate_wallet_data(num_wallets):
    wallets = []
    for _ in range(num_wallets):
        wallet = {
            "Wallet Address": generate_wallet_address(),
            "95. Percentile": f"{random.uniform(95.0, 99.5):.2f}%",
            "Median": f"{random.uniform(92.0, 97.0):.2f}%",
            "5. Percentile": f"{random.uniform(15.0, 25.0):.2f}%",
            "Avg. X Value": f"{random.uniform(120.0, 170.0):.2f}X",
            "Positive Trading Ratio": f"{random.randint(75, 90)}%",
            "Fees": f"${random.randint(1800, 2600)}",
            "Last Activity": generate_last_activity(),
            "Tokens": random.randint(85, 125),
            "Avg. Time Between Transactions": generate_time_delta(3, 5),
            "Max Time Between Transactions": f"{random.randint(4, 6)}d {random.randint(0, 23)}h",
            "Min Time Between Transactions": generate_time_delta(1, 3),
            "Avg. Investments in $": f"${random.randint(3500, 5500)}",
        }
        wallets.append(wallet)
    return wallets


# Function to format the wallet data into a table (plain text for console)
def format_wallet_table(wallets):
    headers = [
        "Wallet Address",
        "95. Percentile",
        "Median",
        "5. Percentile",
        "Avg. X Value",
        "Positive Trading Ratio",
        "Fees",
        "Last Activity",
        "Tokens",
        "Avg. Time Between Transactions",
        "Max Time Between Transactions",
        "Min Time Between Transactions",
        "Avg. Investments in $",
    ]
    table_data = [[wallet[header] for header in headers] for wallet in wallets]
    return tabulate(table_data, headers=headers, tablefmt="grid"), headers, table_data


# Function to generate mock candlestick data for a wallet
def generate_candlestick_data(wallet_index):
    # Generate 60 data points (15-minute intervals over 15 hours)
    start_time = datetime.now() - timedelta(hours=15)
    dates = [start_time + timedelta(minutes=15 * i) for i in range(60)]

    # Simulate price data: dip followed by a rise, with varying ranges for each wallet
    base_price = 1.5 + (
        wallet_index * 0.1
    )  # Starting price varies by wallet (1.5 to 2.4)
    prices = []
    for i in range(60):
        if i < 20:  # Initial decline
            open_price = base_price - (i * 0.003)
            close_price = open_price - random.uniform(0.001, 0.004)
        elif i < 40:  # Bottoming out
            open_price = (base_price - 0.06) + random.uniform(-0.005, 0.005)
            close_price = open_price + random.uniform(-0.005, 0.005)
        else:  # Sharp rise
            open_price = (base_price - 0.06) + ((i - 40) * 0.005)
            close_price = open_price + random.uniform(0.001, 0.006)

        high = max(open_price, close_price) + random.uniform(0.001, 0.003)
        low = min(open_price, close_price) - random.uniform(0.001, 0.003)
        prices.append([open_price, high, low, close_price])

    # Create a DataFrame
    df = pd.DataFrame(
        prices, columns=["Open", "High", "Low", "Close"], index=pd.DatetimeIndex(dates)
    )
    return df


# Function to generate and save a candlestick chart for a wallet with a white background
def generate_candlestick_chart(wallet_index, wallet_address):
    # Generate mock data for the wallet
    df = generate_candlestick_data(wallet_index)

    # Define chart style with a white background
    mpf_style = mpf.make_mpf_style(
        base_mpl_style="default",  # Use default style for white background
        rc={
            "axes.labelcolor": "black",
            "xtick.color": "black",
            "ytick.color": "black",
            "axes.facecolor": "white",
            "figure.facecolor": "white",
        },
        marketcolors=mpf.make_marketcolors(
            up="green", down="red", wick="black", edge="black"
        ),
    )

    # Plot the candlestick chart
    fig, axlist = mpf.plot(
        df,
        type="candle",
        style=mpf_style,
        title=f"Wallet {wallet_index + 1} ({wallet_address[:10]}...) 15m Chart",
        ylabel="Price (USD)",
        figsize=(10, 6),
        returnfig=True,
    )

    # Save the chart as a PNG
    chart_path = f"wallet_{wallet_index + 1}_chart.png"
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)  # Close the figure to free memory
    return chart_path


# Function to convert the wallet table data into an HTML table and include charts
def format_html_table(headers, table_data, chart_paths):
    html = """
    <html>
    <head>
        <style>
            body {
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-family: Arial, sans-serif;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            img {
                max-width: 100%;
                height: auto;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <h2>Profitable Crypto Wallets for Copy Trading</h2>
        <table>
            <tr>
    """
    for header in headers:
        html += f"<th>{header}</th>"
    html += "</tr>"
    for row in table_data:
        html += "<tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>"
    html += """
        </table>
        <h2>Candlestick Charts for Top 10 Wallets</h2>
    """
    # Add charts for the first 10 wallets
    for i, chart_path in enumerate(chart_paths):
        html += f'<img src="cid:wallet_{i + 1}_chart" alt="Wallet {i + 1} Chart"><br>'
    html += """
    </body>
    </html>
    """
    return html


# Function to send the table and charts via email using iCloud
def send_email(
    plain_table,
    html_table,
    chart_paths,
    recipient_email,
    sender_email,
    sender_app_password,
):
    msg = MIMEMultipart("related")  # Use 'related' to embed images
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = f"{EMAIL_SUBJECT_PREFIX} - {datetime.now().strftime('%Y-%m-%d')}"

    # Create an 'alternative' part for plain text and HTML
    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    # Attach the plain text version (fallback)
    msg_alternative.attach(MIMEText(plain_table, "plain"))

    # Attach the HTML version
    msg_alternative.attach(MIMEText(html_table, "html"))

    # Attach the chart images
    for i, chart_path in enumerate(chart_paths):
        with open(chart_path, "rb") as img:
            msg_image = MIMEImage(img.read())
            msg_image.add_header("Content-ID", f"<wallet_{i + 1}_chart>")
            msg.attach(msg_image)

    # Send the email using iCloud's SMTP server
    try:
        with smtplib.SMTP("smtp.mail.me.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        logging.info("Email sent successfully via iCloud!")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


# Main function
def main():
    logging.info("Starting script execution...")

    # Generate wallet data
    wallets = generate_wallet_data(num_wallets=NUM_WALLETS)
    plain_table, headers, table_data = format_wallet_table(wallets)
    logging.info("Generated wallet table.")
    print("Generated Table of Profitable Crypto Wallets for Copy Trading:\n")
    print(plain_table)

    # Generate candlestick charts for the first 10 wallets
    chart_paths = []
    for i in range(min(10, len(wallets))):  # First 10 wallets
        chart_path = generate_candlestick_chart(i, wallets[i]["Wallet Address"])
        chart_paths.append(chart_path)
        logging.info(f"Generated candlestick chart for wallet {i + 1}: {chart_path}")

    # Format the wallet table into HTML and include the charts
    html_table = format_html_table(headers, table_data, chart_paths)

    # Send the email with the table and charts
    send_email(
        plain_table,
        html_table,
        chart_paths,
        RECIPIENT_EMAIL,
        SENDER_EMAIL,
        SENDER_APP_PASSWORD,
    )

    # Clean up chart files
    for chart_path in chart_paths:
        try:
            os.remove(chart_path)
            logging.info(f"Deleted chart file: {chart_path}")
        except Exception as e:
            logging.error(f"Failed to delete chart file {chart_path}: {e}")

    logging.info("Script execution completed.")


if __name__ == "__main__":
    main()
