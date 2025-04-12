from flask import Flask, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

app = Flask(__name__)

# Google AdSense API setup
SCOPES = ["https://www.googleapis.com/auth/adsense.readonly"]
CREDENTIALS_FILE = "credentials.json"  # Download this from Google Cloud Console


def get_adsense_service():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("adsense", "v2", credentials=credentials)


# Fetch AdSense earnings data
def fetch_earnings():
    service = get_adsense_service()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    month_start = today.replace(day=1)
    last_month_end = month_start - datetime.timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # Fetch earnings for different periods
    today_earnings = (
        service.reports()
        .generate(
            startDate=today.strftime("%Y-%m-%d"),
            endDate=today.strftime("%Y-%m-%d"),
            metric=["EARNINGS"],
            dimension=["DATE"],
        )
        .execute()
    )

    yesterday_earnings = (
        service.reports()
        .generate(
            startDate=yesterday.strftime("%Y-%m-%d"),
            endDate=yesterday.strftime("%Y-%m-%d"),
            metric=["EARNINGS"],
            dimension=["DATE"],
        )
        .execute()
    )

    this_month_earnings = (
        service.reports()
        .generate(
            startDate=month_start.strftime("%Y-%m-%d"),
            endDate=today.strftime("%Y-%m-%d"),
            metric=["EARNINGS"],
            dimension=["DATE"],
        )
        .execute()
    )

    last_month_earnings = (
        service.reports()
        .generate(
            startDate=last_month_start.strftime("%Y-%m-%d"),
            endDate=last_month_end.strftime("%Y-%m-%d"),
            metric=["EARNINGS"],
            dimension=["DATE"],
        )
        .execute()
    )

    # Process the earnings (simplified for this example)
    earnings = {
        "today": float(
            today_earnings.get("totals", {}).get("cells", [{}])[0].get("value", 0)
        ),
        "yesterday": float(
            yesterday_earnings.get("totals", {}).get("cells", [{}])[0].get("value", 0)
        ),
        "this_month": float(
            this_month_earnings.get("totals", {}).get("cells", [{}])[0].get("value", 0)
        ),
        "last_month": float(
            last_month_earnings.get("totals", {}).get("cells", [{}])[0].get("value", 0)
        ),
    }
    return earnings


# API endpoint to serve earnings data
@app.route("/api/earnings", methods=["GET"])
def get_earnings():
    try:
        earnings = fetch_earnings()
        return jsonify(earnings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
