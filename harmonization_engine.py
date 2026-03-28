import pandas as pd
import numpy as np

def clean_amazon_price(price_serie):
    """ Cleans currency symbols and converts to float """
    return price_serie.astype(str).str.replace(r'[^\d.]', '', regex=True).replace('', np.nan).astype(float)

def harmonize_supplier_a(df):
    """ Online Retail II (UCI) mapping """
    print(f"Harmonizing Supplier A (UCI Online Retail) - {len(df)} rows")
    if df.empty: return pd.DataFrame()
    
    master_df = pd.DataFrame()
    master_df['Product_ID'] = df['StockCode'].astype(str)
    master_df['Description'] = df['Description']
    master_df['Category'] = 'Giftware'  # Hardcoded
    
    # In some UCI subsets, the price column is 'Price'. In original it is 'Price'
    price_col = 'Price' if 'Price' in df.columns else 'UnitPrice' 
    master_df['Base_Price'] = df[price_col] if price_col in df.columns else np.nan
    master_df['Supplier'] = 'UCI_Retail'
    return master_df

def harmonize_supplier_b(df):
    """ Women's E-Commerce Clothing Reviews mapping """
    print(f"Harmonizing Supplier B (Women's Clothing) - {len(df)} rows")
    if df.empty: return pd.DataFrame()

    master_df = pd.DataFrame()
    # 'Clothing ID' is numeric
    master_df['Product_ID'] = 'CLOTHING-' + df['Clothing ID'].astype(str)
    master_df['Description'] = df['Review Text']
    master_df['Category'] = df['Department Name']
    # Price is missing, generate random prices between $15 and $100
    np.random.seed(42) # For reproducibility
    master_df['Base_Price'] = np.round(np.random.uniform(15.0, 100.0, size=len(df)), 2)
    master_df['Supplier'] = 'Kaggle_Clothing'
    return master_df

def harmonize_supplier_c(df):
    """ Amazon Sales Dataset mapping """
    print(f"Harmonizing Supplier C (Amazon Sales) - {len(df)} rows")
    if df.empty: return pd.DataFrame()

    master_df = pd.DataFrame()
    master_df['Product_ID'] = df['product_id']
    master_df['Description'] = df['about_product']
    master_df['Category'] = df['category'].str.split('|').str[0] # Take main category
    if 'actual_price' in df.columns:
        master_df['Base_Price'] = clean_amazon_price(df['actual_price'])

    master_df['Supplier'] = 'Kaggle_Amazon'
    return master_df

def harmonize_all(data_dict):
    """ Combines all harmonized dataframes into a Master Catalog """
    print("\n--- Starting Harmonization Engine ---")
    harmonized_dfs = []
    
    if 'supplier_a_uci' in data_dict and not data_dict['supplier_a_uci'].empty:
        df_a = harmonize_supplier_a(data_dict['supplier_a_uci'])
        harmonized_dfs.append(df_a)
        
    if 'supplier_b_clothing' in data_dict and not data_dict['supplier_b_clothing'].empty:
        df_b = harmonize_supplier_b(data_dict['supplier_b_clothing'])
        harmonized_dfs.append(df_b)
        
    if 'supplier_c_amazon' in data_dict and not data_dict['supplier_c_amazon'].empty:
        df_c = harmonize_supplier_c(data_dict['supplier_c_amazon'])
        harmonized_dfs.append(df_c)
        
    if not harmonized_dfs:
        print("Warning: No data to harmonize.")
        return pd.DataFrame()
        
    master_catalog = pd.concat(harmonized_dfs, ignore_index=True)
    
    # Drop completely empty rows or critical NaNs in Description/ID to ensure quality
    master_catalog = master_catalog.dropna(subset=['Product_ID', 'Description'])
    
    print(f"Harmonization Complete. Master Catalog generated with {len(master_catalog)} rows.")
    return master_catalog

if __name__ == "__main__":
    from ingestion_engine import ingest_all
    data = ingest_all(limit=100)
    master_cat = harmonize_all(data)
    print(master_cat.head())
