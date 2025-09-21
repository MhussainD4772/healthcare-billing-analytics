#!/usr/bin/env python3
"""
Healthcare Billing Data Loader
Loads Excel data into SQLite database for analysis
"""

import pandas as pd
from sqlalchemy import create_engine
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_excel_to_sqlite(excel_file, db_path):
    """
    Load all Excel sheets into SQLite database
    
    Args:
        excel_file (str): Path to Excel file
        db_path (str): Path to SQLite database
    """
    try:
        # Check if Excel file exists
        if not os.path.exists(excel_file):
            logger.error(f"Excel file not found: {excel_file}")
            return False
        
        logger.info(f"Loading Excel file: {excel_file}")
        
        # Load all sheets from Excel
        sheets = pd.read_excel(excel_file, sheet_name=None)
        logger.info(f"Found {len(sheets)} sheets: {list(sheets.keys())}")
        
        # Create SQLite engine
        db_url = f"sqlite:///{db_path}"
        engine = create_engine(db_url)
        
        # Load each sheet into a separate table
        for sheet_name, df in sheets.items():
            # Clean table name
            table_name = sheet_name.strip().lower().replace(" ", "_").replace("-", "_").replace(",", "")
            
            # Clean column names
            df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_").replace(",", "") for col in df.columns]
            
            # Load to database
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            logger.info(f"✅ Loaded {table_name} ({len(df)} rows)")
        
        logger.info("🎉 Data loading completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return False

if __name__ == "__main__":
    # Configuration
    excel_file = "healthcare_data.xlsx"
    db_path = "healthcare_billing.db"
    
    # Load data
    success = load_excel_to_sqlite(excel_file, db_path)
    
    if success:
        print("✅ Data loaded successfully!")
    else:
        print("❌ Data loading failed!")
