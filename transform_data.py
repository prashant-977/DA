import pandas as pd
import os

def transform_to_shopify(input_file, output_file):
    print(f"Loading cleaned data from {input_file} for transformation...")
    df = pd.read_csv(input_file)
    
    # Mapping to Shopify template columns
    shopify_df = pd.DataFrame()
    
    # We don't have Product_Name anymore, so let's generate one from Description (first 30 chars approx)
    # We will just use the original Product_ID as title if Description is too vague, or a slice of it
    product_titles = df['Description'].astype(str).str.slice(0, 40) + '...'
    
    # Generate Handle from the Product_ID
    shopify_df['Handle'] = df['Product_ID'].astype(str).str.lower().str.replace(r'[^a-zA-Z0-9]', '-', regex=True)
    shopify_df['Title'] = product_titles
    shopify_df['Body (HTML)'] = df['Description']
    shopify_df['Vendor'] = df['Supplier']
    shopify_df['Type'] = df['Category']
    shopify_df['Tags'] = df['Category'].astype(str).apply(lambda x: f"imported, {x}")
    shopify_df['Published'] = 'TRUE'
    
    # Variants mapping
    shopify_df['Option1 Name'] = 'Title'
    shopify_df['Option1 Value'] = 'Default Title'
    shopify_df['Variant SKU'] = df['Product_ID']
    shopify_df['Variant Inventory Tracker'] = 'shopify'
    shopify_df['Variant Inventory Qty'] = 100 # Mocking stock quantity since we don't have it
    shopify_df['Variant Inventory Policy'] = 'deny'
    shopify_df['Variant Fulfillment Service'] = 'manual'
    shopify_df['Variant Price'] = df['Base_Price']
    shopify_df['Variant Requires Shipping'] = 'TRUE'
    shopify_df['Variant Taxable'] = 'TRUE'
    
    # Status
    shopify_df['Status'] = 'active'
    
    shopify_df.to_csv(output_file, index=False)
    print(f"Successfully transformed {len(shopify_df)} records to Shopify Template.")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    if not os.path.exists('clean_data.csv'):
        print("Error: clean_data.csv not found. Please run validate_data.py first.")
    else:
        transform_to_shopify('clean_data.csv', 'shopify_template.csv')
