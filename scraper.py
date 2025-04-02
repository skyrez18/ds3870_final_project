import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_msrp(make, model, year):
    """Fetch MSRP from Edmunds based on make, model, and year."""
    base_url = f"https://www.edmunds.com/{make}/{model}/{year}/features-specs/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data for {year} {make} {model}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        msrp = soup.find('dt', string='MSRP').find_next_sibling('dd').text.strip()
        return msrp
    except AttributeError:
        print(f"MSRP not found for {year} {make} {model}")
        return None

# Load dataset
df = pd.read_csv('vehicle_data.csv')

# Add MSRP column
df['msrp'] = df.apply(lambda row: get_msrp(row['make'], row['model'], row['year']), axis=1)

# Save updated dataset
df.to_csv('vehicle_data_with_msrp.csv', index=False)

print("MSRP scraping complete and dataset updated.")