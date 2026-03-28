import time
import sys
from ingestion_engine import ingest_all
from harmonization_engine import harmonize_all
from validate_data import validate_data
from transform_data import transform_to_shopify
from excel_export import generate_excel_report
from database_operations import setup_database, run_inventory_reports
from api_upload import simulate_api_upload

def main():
    print("="*60)
    print("  E-COMMERCE CATALOG SYNC & QUALITY ENGINE - RUN PIPELINE")
    print("="*60)
    
    start_time = time.time()
    
    # 1. Ingest Data
    print("\n[Step 1] Initializing Extensible Ingestion Layer...")
    # Using a 100 limit here for fast portfolio demonstration. Change if you want full size.
    raw_data_dict = ingest_all(limit=100) 
    
    # 2. Harmonize Data
    print("\n[Step 2] Formatting through Harmonization Engine...")
    master_catalog = harmonize_all(raw_data_dict)
    
    if master_catalog.empty:
        print("Pipeline Aborted: No valid data harmonized.")
        sys.exit(1)
        
    master_catalog.to_csv("master_catalog.csv", index=False)
    print(f"Master Catalog Saved: master_catalog.csv")
    
    # 3. Validate Data
    print("\n[Step 3] Running Validation Protocols...")
    validate_data('master_catalog.csv', 'clean_data.csv', 'quarantine_report.csv')
    
    # 4. Transform to Shopify API
    print("\n[Step 4] Transforming Clean Data to Marketplace Template...")
    transform_to_shopify('clean_data.csv', 'shopify_template.csv')
    
    # 5. Advanced Excel Cross Check
    print("\n[Step 5] Generating Advanced Excel Pricing Cross-Check...")
    try:
        clean_df = __import__('pandas').read_csv('clean_data.csv')
        generate_excel_report(clean_df, "Master_Catalog_CrossCheck.xlsx")
    except Exception as e:
        print(f"Failed to generate Excel report: {e}")
        
    # 6. Database Load & Reports
    print("\n[Step 6] Persisting to SQLite & Running Analysis Reports...")
    conn = setup_database('master_catalog.db', 'clean_data.csv')
    if conn:
        run_inventory_reports(conn)
        conn.close()
        
    # 7. Simulated API Upload
    print("\n[Step 7] Simulating JSON REST API Upload...")
    simulate_api_upload('shopify_template.csv')
    
    end_time = time.time()
    print("\n="*60)
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {round(end_time - start_time, 2)} SECONDS.")
    print("="*60)
    
if __name__ == "__main__":
    main()
