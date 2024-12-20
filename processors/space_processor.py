import os
import sys
import pandas as pd

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.error_handler import handle_error, logger

@handle_error
def process_space_data(asset_location_file, space_template, namespace):
    """Process space data"""
    logger.info("Starting space data processing")
    
    # Load data
    asset_location_data = pd.read_excel(asset_location_file, sheet_name='Asset,location')
    template_data = pd.read_csv(space_template)
    
    # Extract unique data
    unique_data = asset_location_data[['Building', 'Floor', 'Sublocation']].drop_duplicates().dropna()
    valid_data = unique_data[
        (unique_data['Building'] != 'Mandatory') &
        (unique_data['Building'].notna()) &
        (unique_data['Floor'] != 'Mandatory') &
        (unique_data['Floor'].notna()) &
        (unique_data['Sublocation'] != 'Mandatory') &
        (unique_data['Sublocation'].notna())
    ]
    
    # Create new space data
    new_space_data = pd.DataFrame({
        'facility name': valid_data['Building'].reset_index(drop=True),
        'location name': valid_data['Floor'].reset_index(drop=True),
        'name*': valid_data['Sublocation'].reset_index(drop=True),
        'namespace*': namespace,
        'isActive*': True
    })
    
    # Merge with template
    template_data_cleaned = template_data.iloc[1:]
    updated_space_data = pd.concat([template_data_cleaned, new_space_data], ignore_index=True)
    
    logger.info(f"Processed {len(new_space_data)} space records")
    return updated_space_data
