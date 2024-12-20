import os
import sys
import pandas as pd

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.error_handler import handle_error, logger

@handle_error
def process_location_data(asset_location_file, location_template, namespace):
    """Process location data"""
    logger.info("Starting location data processing")
    
    # Load files
    asset_location_data = pd.read_excel(asset_location_file, sheet_name='Asset,location')
    template_data = pd.read_csv(location_template)
    
    # Extract and clean building/floor data
    unique_building_floor = asset_location_data[['Building', 'Floor']].drop_duplicates().dropna()
    valid_data = unique_building_floor[
        (unique_building_floor['Building'] != 'Mandatory') & 
        (unique_building_floor['Building'].notna()) & 
        (unique_building_floor['Floor'] != 'Mandatory') & 
        (unique_building_floor['Floor'].notna())
    ]
    
    # Create new location data
    new_location_data = pd.DataFrame({
        'facility*': [None] * len(valid_data),
        'facility name': valid_data['Building'].reset_index(drop=True),
        'name*': valid_data['Floor'].reset_index(drop=True),
        'namespace*': namespace,
        'isActive*': True
    })
    
    # Merge with template
    template_data_cleaned = template_data.iloc[1:]
    updated_location_data = pd.concat([template_data_cleaned, new_location_data], ignore_index=True)
    
    logger.info(f"Processed {len(new_location_data)} location records")
    return updated_location_data
