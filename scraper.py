import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('msrp_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def format_for_url(text):
    """Convert text to URL-friendly format"""
    text = text.lower().replace(" ", "-")
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def create_session():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    retry_adapter = requests.adapters.HTTPAdapter(
        max_retries=3,
        pool_connections=10,
        pool_maxsize=10
    )
    session.mount('https://', retry_adapter)
    return session

def extract_msrp(soup):
    """Try multiple methods to extract MSRP from page"""
    selectors = [
        ('dt', 'MSRP'),  # Primary selector
        ('span', {'class': 'price-value'}),
        ('div', {'class': 'price-wrapper'}),
        ('span', {'itemprop': 'price'})
    ]
    
    for tag, identifier in selectors:
        try:
            if isinstance(identifier, str):
                element = soup.find(tag, string=identifier)
                if element and (sibling := element.find_next_sibling('dd')):
                    return sibling.text.strip()
            else:
                if element := soup.find(tag, identifier):
                    return element.text.strip()
        except Exception:
            continue
    return None

def get_msrp(make, model, year, session):
    """Fetch MSRP with comprehensive error handling"""
    make_fmt = format_for_url(make)
    model_fmt = format_for_url(model)
    url = f"https://www.edmunds.com/{make_fmt}/{model_fmt}/{year}/features-specs/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.edmunds.com/"
    }

    try:
        # Random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        if msrp := extract_msrp(soup):
            logger.info(f"Success: {year} {make} {model} - MSRP: {msrp}")
            return msrp
        else:
            logger.warning(f"MSRP not found: {year} {make} {model}")
            return pd.NA
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {year} {make} {model} - {str(e)}")
        return pd.NA
    except Exception as e:
        logger.error(f"Unexpected error: {year} {make} {model} - {str(e)}")
        return pd.NA

def process_row(row, session):
    """Wrapper function for parallel processing"""
    return get_msrp(row['make'], row['model'], row['year'], session)

def main(input_file, output_file, max_workers=5):
    """Main execution flow"""
    try:
        # Read input
        df = pd.read_csv(input_file)
        if 'msrp' not in df.columns:
            df['msrp'] = pd.NA
        
        # Initialize session
        session = create_session()
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_row, row, session): idx
                for idx, row in df.iterrows()
                if pd.isna(row['msrp'])  # Only process rows without MSRP
            }
            
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    df.at[idx, 'msrp'] = future.result()
                except Exception as e:
                    logger.error(f"Result handling failed for row {idx}: {str(e)}")
                    df.at[idx, 'msrp'] = pd.NA
        
        # Save results
        df.to_csv(output_file, index=False)
        logger.info(f"Successfully saved results to {output_file}")
        print(f"\nProcessing complete. Results saved to {output_file}")
        print(f"Success rate: {df['msrp'].notna().mean():.1%}")
        
    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    # Configuration
    INPUT_CSV = 'vehicle_data.csv'
    OUTPUT_CSV = 'vehicle_data_with_msrp.csv'
    WORKERS = 5  # Conservative default
    
    print(f"Starting MSRP scraping for {INPUT_CSV}")
    print(f"Using {WORKERS} parallel workers")
    print("Logging detailed progress to msrp_scraper.log\n")
    
    main(input_file=INPUT_CSV, output_file=OUTPUT_CSV, max_workers=WORKERS)