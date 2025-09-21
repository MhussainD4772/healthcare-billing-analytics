# Database Configuration
DATABASE_CONFIG = {
    'type': 'sqlite',
    'path': 'healthcare_billing.db',
    'url': 'sqlite:///healthcare_billing.db'
}

# Excel Configuration
EXCEL_CONFIG = {
    'file_path': 'healthcare_data.xlsx',
    'sheet_names': None  # Load all sheets
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'output_dir': 'output',
    'chart_format': 'png',
    'chart_dpi': 300
}
