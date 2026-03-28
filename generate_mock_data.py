import pandas as pd
import numpy as np
import random
import os

def generate_mock_dataset():
    # Simulate realistic dirty data
    data = []
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Toys']
    suppliers = ['SUP_A', 'SUP_B', 'SUP_C']
    
    # We want reproducible mock data
    random.seed(42)
    np.random.seed(42)
    
    for i in range(1, 101):
        # 10% chance of negative price
        price = round(random.uniform(5.0, 150.0), 2)
        if random.random() < 0.1:
            price = -price
            
        # 15% chance of missing description
        desc = f"Great product {i} for your needs. Highly recommended."
        if random.random() < 0.15:
            desc = np.nan
            
        # 10% chance of wrong SKU format (should start with SKU-)
        sku = f"SKU-{1000 + i}"
        if random.random() < 0.1:
            sku = f"BAD-{1000 + i}"
            
        row = {
            'Supplier_ID': random.choice(suppliers),
            'SKU': sku,
            'Product_Name': f"Product {i}",
            'Description': desc,
            'Price': price,
            'Category': random.choice(categories),
            'Stock_Quantity': random.randint(0, 500)
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    df.to_csv('raw_supplier_data.csv', index=False)
    print(f"Generated raw_supplier_data.csv with {len(df)} rows.")

if __name__ == "__main__":
    generate_mock_dataset()
