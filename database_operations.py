import sqlite3
import pandas as pd
import os

def setup_database(db_name, input_file):
    print(f"Connecting to SQLite database: {db_name}")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create inventory table matching Master Catalog schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier TEXT,
            product_id TEXT,
            description TEXT,
            category TEXT,
            base_price REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Load clean data
    print(f"Loading data from {input_file} into SQLite...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error loading {input_file}: {e}")
        return
        
    db_df = df.rename(columns={
        'Supplier': 'supplier',
        'Product_ID': 'product_id',
        'Description': 'description',
        'Category': 'category',
        'Base_Price': 'base_price'
    })
    
    # Replace the existing entries
    db_df.to_sql('inventory', conn, if_exists='replace', index=False)
    print("Data inserted successfully.")
    
    return conn

def run_inventory_reports(conn):
    print("\n--- Daily Database Reports ---")
    
    # Query 1: Total Products per Category
    print("\n1. Total Products per Category (Top 5):")
    query1 = """
        SELECT category, COUNT(product_id) as total_products
        FROM inventory
        GROUP BY category
        ORDER BY total_products DESC
        LIMIT 5;
    """
    df1 = pd.read_sql_query(query1, conn)
    print(df1.to_string(index=False))
    
    # Query 2: Product Count and Average Price by Supplier
    print("\n2. Product Count and Average Base Price by Supplier:")
    query2 = """
        SELECT supplier, COUNT(product_id) as total_products, ROUND(AVG(base_price), 2) as avg_price
        FROM inventory
        GROUP BY supplier
        ORDER BY total_products DESC;
    """
    df2 = pd.read_sql_query(query2, conn)
    print(df2.to_string(index=False))
        
    # Query 3: Most Expensive Items
    print("\n3. Top 5 Most Expensive Items in Catalog:")
    query3 = """
        SELECT product_id, category, base_price, supplier
        FROM inventory
        ORDER BY base_price DESC
        LIMIT 5;
    """
    df3 = pd.read_sql_query(query3, conn)
    print(df3.to_string(index=False))
    
    print("\n-------------------------------")

if __name__ == "__main__":
    if not os.path.exists('clean_data.csv'):
        print("Error: clean_data.csv not found. Please run validate_data.py first.")
    else:
        conn = setup_database('master_catalog.db', 'clean_data.csv')
        if conn:
            run_inventory_reports(conn)
            conn.close()
