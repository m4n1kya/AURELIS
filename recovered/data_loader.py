import pandas as pd
import os

def load_data(data_dir: str):
    \"\"\"Loads all CSVs into a dictionary of DataFrames.\"\"\"
    data = {}
    csv_files = [
        \"financial_profiles.csv\",
        \"financial_events.csv\",
        \"exchange_rates.csv\",
        \"request_payment_options.csv\",
        \"messages.csv\",
        \"images.csv\",
        \"requests.csv\",
        \"sample_requests.csv\"
    ]
    for filename in csv_files:
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            data[filename.replace(\".csv\", \"\")] = pd.read_csv(path)
        else:
            print(f\"Warning: {path} not found.\")
            data[filename.replace(\".csv\", \"\")] = pd.DataFrame()
            
    # Also create a dummy output template if needed
    return data

