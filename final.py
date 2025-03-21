# Sky Reznik, John Lackey, Kevin Abatto
# Packages
import pandas as pd 
import numpy as np 
# Import data 
import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Specify the dataset and the path to save it
dataset_name = 'tunguz/used-car-auction-prices'  # Replace with your actual Kaggle dataset name
download_path = './kaggle_datasets'     # Folder to store the dataset

# Create download path if it doesn't exist
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Check if the dataset already exists in the folder
dataset_file_path = os.path.join(download_path, 'dataset.csv')  # Modify this based on the dataset file
if not os.path.exists(dataset_file_path):
    # Initialize the Kaggle API
    api = KaggleApi()
    api.authenticate()  # Authenticate using your Kaggle credentials

    # Download the dataset
    print(f"Downloading {dataset_name}...")
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)

    print("Download complete.")
else:
    print("Dataset already exists, skipping download.")

# Load CSV into a pandas dataframe
shared_file_path = './kaggle_datasets/used-car-auction-prices/car_prices.csv'
df = pd.read_csv(shared_file_path)
print(df.head())