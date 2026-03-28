import pandas as pd
import numpy as np

def generate_excel_report(master_df, output_path="Master_Catalog_CrossCheck.xlsx"):
    print(f"\n--- Generating Advanced Excel Report: {output_path} ---")
    
    # 1. Create a Price Benchmark dataset
    # We will use the unique categories from the master_df, and assign an average mock price
    unique_categories = master_df['Category'].dropna().unique()
    np.random.seed(42) # Reproducibility
    
    benchmark_df = pd.DataFrame({
        'Category': unique_categories,
        'Market_Average': np.round(np.random.uniform(20.0, 150.0, size=len(unique_categories)), 2)
    })
    
    # Sort for cleaner lookup although not strictly required for XLOOKUP/VLOOKUP in FALSE/Exact mode
    benchmark_df = benchmark_df.sort_values(by='Category')

    # 2. Write to Excel using xlsxwriter
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    
    # Write the Master Catalog
    master_df.to_excel(writer, sheet_name='Master_Catalog', index=False)
    
    # Write the Price Benchmark
    benchmark_df.to_excel(writer, sheet_name='Price_Benchmark', index=False)
    
    # 3. Access the workbook and worksheet objects to apply advanced formatting
    workbook = writer.book
    worksheet_master = writer.sheets['Master_Catalog']
    worksheet_benchmark = writer.sheets['Price_Benchmark']
    
    # Formats
    currency_format = workbook.add_format({'num_format': '$#,##0.00'})
    red_highlight = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    bold = workbook.add_format({'bold': True})
    
    num_rows = len(master_df)
    
    if num_rows > 0:
        # VLOOKUP Formula: Look up 'Category' in the 'Price_Benchmark' sheet
        # Assuming Category is column C (index 2) in Master_Catalog
        # Formula: =VLOOKUP(C2, Price_Benchmark!$A$2:$B$100, 2, FALSE)
        
        bench_rows = len(benchmark_df) + 1
        
        # Add 'Market_Average' column headers in Master_Catalog sheet
        worksheet_master.write(0, 5, "Market_Average", bold)
        worksheet_master.write(0, 6, "20%_Markup_Threshold", bold)
        worksheet_master.write(0, 7, "Overpriced_Status", bold)
        
        for row_num in range(1, num_rows + 1):
            category_cell = f'C{row_num + 1}'
            vlookup_formula = f'=VLOOKUP({category_cell}, Price_Benchmark!$A$2:$B${bench_rows}, 2, FALSE)'
            worksheet_master.write_formula(row_num, 5, vlookup_formula, currency_format)
            
            # Threshold = 1.2 * Market_Average (Column F is index 5)
            threshold_formula = f'=F{row_num + 1} * 1.2'
            worksheet_master.write_formula(row_num, 6, threshold_formula, currency_format)
            
            # Status: IF Base_Price > Threshold
            # Base_Price is column D (index 3)
            base_price_cell = f'D{row_num + 1}'
            threshold_cell = f'G{row_num + 1}'
            status_formula = f'=IF({base_price_cell}>{threshold_cell}, "Overpriced", "Okay")'
            worksheet_master.write_formula(row_num, 7, status_formula)
            
            # Write Base_Price (column D) with Currency Format
            value = master_df.iloc[row_num - 1]['Base_Price'] if not pd.isna(master_df.iloc[row_num - 1]['Base_Price']) else 0
            worksheet_master.write_number(row_num, 3, float(value), currency_format)

        # 4. Conditional Formatting on the Base_Price column
        # Highlight cells in Base_Price (D) that are > than their corresponding Threshold (G)
        worksheet_master.conditional_format(f'D2:D{num_rows+1}', {
            'type': 'formula',
            'criteria': f'=D2>G2', # Note format is relative to the top left of the range
            'format': red_highlight
        })
        
        # Autofit columns for readability
        worksheet_master.autofit()
        worksheet_benchmark.autofit()

    writer.close()
    print(f"Excel Customization complete. Benchmark prices checked through VLOOKUP and conditionally formatted if 20% over market.")

if __name__ == "__main__":
    # Test
    df = pd.DataFrame({"Product_ID": ["A", "B"], "Description": ["Desc1", "Desc2"], "Category": ["Giftware", "Toys"], "Base_Price": [120.0, 5.0]})
    generate_excel_report(df, "test_excel_vlookup.xlsx")
