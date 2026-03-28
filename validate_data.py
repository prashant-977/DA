import pandas as pd
import os

def validate_data(input_file, clean_out, quarantined_out):
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Validation Rules for the Master Catalog
    # 1. Base_Price must be > 0
    # 2. Product_ID must not be missing
    # 3. Description must not be missing
    
    valid_price = df['Base_Price'] > 0
    valid_sku = df['Product_ID'].notna() & (df['Product_ID'] != "")
    valid_desc = df['Description'].notna()
    
    # Clean data must meet ALL criteria
    clean_mask = valid_price & valid_sku & valid_desc
    clean_df = df[clean_mask]
    
    # Quarantined data is everything that fails
    quarantined_df = df[~clean_mask].copy()
    
    # Add a reason column for quarantined data
    reasons = []
    for _, row in quarantined_df.iterrows():
        reason = []
        if pd.isna(row['Base_Price']) or row['Base_Price'] <= 0:
            reason.append("Invalid Base_Price")
        if pd.isna(row['Product_ID']) or str(row['Product_ID']).strip() == "":
            reason.append("Missing/Invalid Product_ID")
        if pd.isna(row['Description']):
            reason.append("Missing Description")
        reasons.append(" | ".join(reason))
        
    quarantined_df['Quarantine_Reason'] = reasons
    
    clean_df.to_csv(clean_out, index=False)
    quarantined_df.to_csv(quarantined_out, index=False)
    
    print(f"Data Validation Complete.")
    print(f"Total Processed: {len(df)}")
    print(f"Clean Records: {len(clean_df)}")
    print(f"Quarantined Records: {len(quarantined_df)}")
    
if __name__ == "__main__":
    if not os.path.exists('master_catalog.csv'):
        print("Error: master_catalog.csv not found. Please run harmonization_engine.py first.")
    else:
        validate_data('master_catalog.csv', 'clean_data.csv', 'quarantine_report.csv')
