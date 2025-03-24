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

# Check if file exists
dataset_file_path = os.path.join(download_path, 'car_prices.csv')   
# Check if the dataset already exists in the folder
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
shared_file_path = './kaggle_datasets/car_prices.csv'
# line 408,163 - "Model" field contains a comma (SE PZEV w/Connectivity, Navigation) - specify quotechar='"'
# This tells Pandas to treat anything inside double quotes as a single field, even if it contains commas.
#      solution provided by ChatGPT
df = pd.read_csv(shared_file_path, quotechar='"', on_bad_lines='skip')
#print(df.head())



# Data Cleaning
print("Start: ", df.shape)
# Remove any row with missing data
df = df.dropna()
print("Finish: ", df.shape)


'''
# Plot 'mmr' v. 'sellingprice'
import matplotlib.pyplot as plt
import seaborn as sns
# Set the style of seaborn
sns.set(style="whitegrid")
plt.scatter(df['mmr'], df['sellingprice']) # Create a scatter plot
sns.regplot(x='mmr', y='sellingprice', data=df, scatter=False, color='red') # Linear fit line
plt.title('MMR vs Selling Price')
plt.xlabel('MMR')
plt.ylabel('Selling Price')
plt.show()
'''



# Scatter plot is showing so outlires, lets take a closer looke at the data to find and remove them

outliers_rows = df.index[
    ((df['mmr'] > 100000) | (df['sellingprice'] > 100000)) &
    ((df['mmr'] > df['sellingprice'] * 2) | (df['mmr'] < df['sellingprice'] * 0.5))
].tolist()

print("Outliers: ", outliers_rows)
print(df.loc[outliers_rows])
