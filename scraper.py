import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def format_for_url(text):
    """Convert text to Edmunds URL format (lowercase, hyphens, no special chars)."""
    text = text.lower().replace(" ", "-")  # Replace spaces with hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)  # Remove special characters
    return text

def get_msrp(make, model, year, retries=3):
    """Fetch MSRP from Edmunds based on make, model, and year, with retries."""
    make = format_for_url(make)
    model = format_for_url(model)
    base_url = f"https://www.edmunds.com/{make}/{model}/{year}/features-specs/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for attempt in range(retries):
        try:
            response = requests.get(base_url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                msrp = soup.find('dt', string='MSRP').find_next_sibling('dd').text.strip()
                return msrp
            else:
                print(f"Attempt {attempt+1}: Failed to fetch {year} {make} {model}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Attempt {attempt+1}: Error fetching {year} {make} {model}: {e}")
        time.sleep(2)  # Delay before retry
    return None

def process_row(row):
    return get_msrp(row['make'], row['model'], row['year'])

# Load dataset
df = pd.read_csv('vehicle_data.csv')

# Use ThreadPoolExecutor for parallel requests
num_workers = 10  # Adjust based on your system performance
results = []

with ThreadPoolExecutor(max_workers=num_workers) as executor:
    future_to_index = {executor.submit(process_row, row): idx for idx, row in df.iterrows()}
    for future in as_completed(future_to_index):
        idx = future_to_index[future]
        try:
            df.at[idx, 'msrp'] = future.result()
        except Exception as e:
            print(f"Error processing row {idx}: {e}")

# Save updated dataset
df.to_csv('vehicle_data_with_msrp.csv', index=False)

print("MSRP scraping complete and dataset updated.")
