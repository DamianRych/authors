import pandas as pd
from datetime import datetime
import sys
import os

csv_path = 'merchsloth/post_dates.csv'

# Ensure the CSV file exists
if not os.path.exists(csv_path):
    print(f"::error::CSV file {csv_path} not found. Please create it.")
    sys.exit(1)

# Load the CSV file
try:
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("CSV file is empty.")
except Exception as e:
    print(f"::error::Failed to read CSV file: {e}")
    sys.exit(1)

# Get the latest date from the CSV
try:
    latest_date = pd.to_datetime(df.iloc[-1, 0]).date()
except IndexError:
    print("::error::CSV file does not contain valid data.")
    sys.exit(1)

# Get today's date
today = datetime.today().date()

if latest_date != today:
    # Append today's date to the CSV
    new_row = pd.DataFrame([[today.strftime('%Y-%m-%d')]], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_path, index=False)
    
    print(f"::error::Make a post for Merchsloth for {today.strftime('%Y-%m-%d')}")
    sys.exit(1)  # Fail the action
else:
    print("Latest post date is up to date.")
