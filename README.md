# Automated E-commerce Catalog Sync & Quality Engine

## Overview
This project simulates a real-world data engineering and integrations pipeline. It features an **Extensible Ingestion Layer** that programmatically fetches messy product data from diverse, real-world suppliers (UCI Machine Learning Repository and Kaggle), harmonizes it, validates it, and transforms it for an e-commerce platform like Shopify. Furthermore, it simulates a backend API integration, stores the "Golden Records" in an SQLite database, and outputs an **Advanced Excel Cross-Check** report containing `VLOOKUP` and conditional formatting.

## The Problem
Inconsistent product data formats across different suppliers (missing SKU identifiers, unpredictable schemas, varying pricing) lead to lost sales and operational lag. Additionally, tracking these prices against a predefined "Market Average" for profitability is often done through tedious manual Excel work.

## The Solution
Built an automated pipeline that acts as an "Ingestion Engine," "Gatekeeper," "Transformer," and "Reporter":
- **Programmatic Ingestion**: Automatically pulls data from remote data lakes/APIs instead of relying on manual downloads.
- **Harmonization**: Merges different data schemas (UCI, Kaggle sources) into a localized "Master Catalog".
- **Advanced Excel Reporting**: Fully automates the creation of a competitive pricing cross-check file using `pandas` and `xlsxwriter` to inject `VLOOKUP` logic and conditional formatting directly into the output files for business stakeholders.

## Tech Stack
- **Python (Pandas & Numpy)**: Used for data ingestion, cleaning, complex transformations, and price engineering.
- **`ucimlrepo` & `kagglehub`**: Connectors used to programmatically fetch multi-source datasets.
- **`xlsxwriter` / `openpyxl`**: Powers the dynamic generation of Excel files complete with native Excel formulas and conditional formatting rules.
- **SQLite**: Stores the Master Catalog for reliable downstream querying.
- **Requests Library**: Simulates pushing the formatted data to a REST API.

## Pipeline Steps
1. **Extensible Ingestion (`ingestion_engine.py`)**: Fetches massive datasets from external sources (UCI's Online Retail II, Kaggle's Amazon Sales, Kaggle's Women's E-Commerce Reviews). 
2. **Harmonization (`harmonization_engine.py`)**: Normalizes disparate supplier columns (e.g. `StockCode`, `Clothing ID`, `product_id`) into a strict standardized `Master Catalog`.
3. **Data Validation (`validate_data.py`)**: Scrubs the Master Catalog, checking for invalid prices and missing identifiers.
4. **Marketplace Transformation (`transform_data.py`)**: Maps the clean dataset into the strict Shopify inventory template format, saving to `shopify_template.csv`.
5. **Advanced Excel Output (`excel_export.py`)**: Takes the master data, generates a competitive Price Benchmark sheet, injects `VLOOKUP` formulas into the catalog sheet to fetch those benchmarks, and applies Conditional Formatting to highlight products priced 20% over the market average.
6. **Database Storage & Reporting (`database_operations.py`)**: Pushes the clean product catalog to a SQLite database (`master_catalog.db`) and runs aggregate analytical queries.
7. **API Integration (`api_upload.py`)**: Simulates POST requests to a backend API.

## How to Run

Ensure you have the required dependencies:
```bash
pip install pandas numpy requests openpyxl xlsxwriter ucimlrepo kagglehub
```
*(Note: Pulling from Kaggle may require your API credentials located in `~/.kaggle/kaggle.json`)*

Run the orchestrated pipeline:
```bash
python run_pipeline.py
```

## NB: 
The ```generate_mock_data.py``` should be run first to generate the necessary files (csv).
