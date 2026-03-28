import pandas as pd
from ucimlrepo import fetch_ucirepo
import kagglehub
import os
import glob

def fetch_uci_retail(limit=5000):
    print("Fetching UCI Online Retail II dataset...")
    try:
        online_retail = fetch_ucirepo(id=502)
        df = online_retail.data.original
        print(f"Successfully fetched UCI dataset: {len(df)} rows.")
        return df.head(limit) if limit else df
    except Exception as e:
        print(f"Failed to fetch UCI dataset: {e}")
        return pd.DataFrame()

def fetch_kaggle_womens_clothing(limit=5000):
    print("Fetching Kaggle Women's E-Commerce Clothing Reviews...")
    try:
        path = kagglehub.dataset_download("nicapotato/womens-ecommerce-clothing-reviews")
        # Find the CSV file in the downloaded path
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        if not csv_files:
            print("No CSV found in Kaggle download for Women's Clothing.")
            return pd.DataFrame()
        
        df = pd.read_csv(csv_files[0], nrows=limit if limit else None)
        print(f"Successfully loaded {len(df)} rows from Women's Clothing reviews.")
        return df
    except Exception as e:
        print(f"Failed to fetch Women's Clothing dataset: {e}")
        print("Note: Kaggle API credentials may be required (~/.kaggle/kaggle.json)")
        return pd.DataFrame()

def fetch_kaggle_amazon_sales(limit=5000):
    print("Fetching Kaggle Amazon Sales Dataset...")
    try:
        path = kagglehub.dataset_download("karkavelrajaj/amazon-sales-dataset")
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        if not csv_files:
            print("No CSV found in Kaggle download for Amazon Sales.")
            return pd.DataFrame()
            
        df = pd.read_csv(csv_files[0], nrows=limit if limit else None)
        print(f"Successfully loaded {len(df)} rows from Amazon Sales dataset.")
        return df
    except Exception as e:
        print(f"Failed to fetch Amazon Sales dataset: {e}")
        print("Note: Kaggle API credentials may be required (~/.kaggle/kaggle.json)")
        return pd.DataFrame()

def ingest_all(limit=5000):
    print(f"--- Starting Ingestion Engine (Limit: {limit} rows per source) ---")
    data = {}
    data['supplier_a_uci'] = fetch_uci_retail(limit)
    data['supplier_b_clothing'] = fetch_kaggle_womens_clothing(limit)
    data['supplier_c_amazon'] = fetch_kaggle_amazon_sales(limit)
    return data

if __name__ == "__main__":
    # Test the ingestion
    ingested_data = ingest_all(limit=100)
    for source, df in ingested_data.items():
        print(f"{source}: {df.shape}")
