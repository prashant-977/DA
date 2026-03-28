import pandas as pd
import requests
import json
import time
import logging
import os

# Set up logging
logging.basicConfig(
    filename='api_upload.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def simulate_api_upload(input_file):
    print(f"Starting API upload simulation using {input_file}...")
    logging.info(f"Starting API upload process for {input_file}")
    
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        logging.error(f"Failed to read input file: {e}")
        return
        
    # We will use JSONPlaceholder to simulate a POST backend request
    API_URL = "https://jsonplaceholder.typicode.com/posts"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    success_count = 0
    failure_count = 0
    
    # For demonstration, upload 5 sample records
    records_to_upload = df.head(5).to_dict('records')
    print(f"Attempting to upload {len(records_to_upload)} sample records to {API_URL}...")
    
    for record in records_to_upload:
        payload = {
            "title": record.get('Title', 'Unknown Product'),
            "body": record.get('Body (HTML)', ''),
            "userId": 1, # Mock User ID
            "metadata": record
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
            if response.status_code in [200, 201]:
                logging.info(f"Successfully simulated upload for Product ID: {record.get('Variant SKU')}. Response ID: {response.json().get('id')}")
                success_count += 1
            else:
                logging.warning(f"Failed upload for Product ID: {record.get('Variant SKU')}. Status Code: {response.status_code}")
                failure_count += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"API Request failed for Product ID: {record.get('Variant SKU')}. Error: {e}")
            failure_count += 1
            
        # Optional: slight delay
        time.sleep(0.5)
        
    print("API Upload Simulation Complete!")
    print(f"Successful Uploads: {success_count}")
    print(f"Failed Uploads: {failure_count}")
    print("Check api_upload.log for detailed execution traces.")
    
if __name__ == "__main__":
    if not os.path.exists('shopify_template.csv'):
        print("Error: shopify_template.csv not found. Run transform_data.py first.")
    else:
        simulate_api_upload('shopify_template.csv')
