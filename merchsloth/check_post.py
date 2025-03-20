import pandas as pd
from datetime import datetime, timedelta
import sys
import os

csv_path = 'merchsloth/post_dates.csv'

# Ensure the CSV file exists or create it with the correct header
if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
    df = pd.DataFrame(columns=["Dates"])
    df.to_csv(csv_path, index=False)
else:
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            df = pd.DataFrame(columns=["Dates"])
            df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"::error::Failed to read CSV file: {e}")
        sys.exit(1)

# Get the latest date from the CSV (if any data exists)
try:
    latest_date = pd.to_datetime(df.iloc[-1, 0]).date()
except IndexError:
    # If there's no valid data, set latest_date to a past date (e.g., 30 days ago)
    latest_date = datetime.today().date() - timedelta(days=30)

# Get today's date
today = datetime.today().date()

if latest_date != today:
    # Append today's date to the CSV
    new_row = pd.DataFrame([[today.strftime('%Y-%m-%d')]], columns=["Dates"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_path, index=False)
    
    print(f"::error::Make a post for Merchsloth for {today.strftime('%Y-%m-%d')}")
    sys.exit(0)  # Fail the action
else:
    print("Latest post date is up to date.")
    sys.exit(0)
