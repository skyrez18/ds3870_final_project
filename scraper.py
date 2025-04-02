import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_for_url(text):
    """Convert text to Edmunds URL format (lowercase, hyphens, no special chars)."""
    text = text.lower().replace(" ", "-")  # Replace spaces with hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)  # Remove special characters
    return text

def get_msrp(make, model, year, session, retries=3):
    """Fetch MSRP from Edmunds based on make, model, and year, with retries."""
    make = format_for_url(make)
    model = format_for_url(model)
    base_url = f"https://www.edmunds.com/{make}/{model}/{year}/features-specs/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for attempt in range(retries):
        try:
            response = session.get(base_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                msrp_label = soup.find('dt', string='MSRP')
                
                if not msrp_label:
                    logger.warning(f"MSRP label not found for {year} {make} {model}")
                    return None
                    
                msrp_value = msrp_label.find_next_sibling('dd')
                if not msrp_value:
                    logger.warning(f"MSRP value not found for {year} {make} {model}")
                    return None
                    
                return msrp_value.text.strip()
            else:
                logger.warning(f"Attempt {attempt+1}: Failed to fetch {year} {make} {model}, Status Code: {response.status_code}")
        except Exception as e:
            logger.error(f"Attempt {attempt+1}: Error fetching {year} {make} {model}: {str(e)}")
        time.sleep(2 ** attempt)  # Exponential backoff
        
    return None

def process_row(row, session):
    return get_msrp(row['make'], row['model'], row['year'], session)

def main():
    # Load dataset
    try:
        shared_file_path = './kaggle_datasets/car_prices.csv'
        df = pd.read_csv(shared_file_path, quotechar='"', on_bad_lines='skip')
    except Exception as e:
        logger.error(f"Failed to load CSV file: {str(e)}")
        return

    # Initialize session and results
    results = []
    num_workers = 10  # Adjust based on your system and network conditions
    
    with requests.Session() as session, ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(process_row, row, session): idx 
            for idx, row in df.iterrows()
        }
        
        # Process completed tasks
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                df.at[idx, 'msrp'] = future.result()
                # Small delay to be polite to the server
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error processing row {idx}: {str(e)}")

    # Save updated dataset
    try:
        df.to_csv('vehicle_data_with_msrp.csv', index=False)
        logger.info("MSRP scraping complete and dataset updated.")
    except Exception as e:
        logger.error(f"Failed to save results: {str(e)}")

if __name__ == "__main__":
    main()