import os
import sys
import pandas as pd

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.error_handler import handle_error, logger

@handle_error
def process_system_asset_mapping(location_file, space_file):
    """Process system asset ID mapping"""
    logger.info("Starting system asset ID mapping")
    
    # Load the files
    location_data = pd.read_csv(location_file)
    space_data = pd.read_csv(space_file)

    # Clean the relevant columns
    location_data['name_cleaned'] = location_data['name*'].str.strip()
    space_data['asset_name_cleaned'] = space_data['asset name'].astype(str).str.strip()

    # Create mapping dictionary
    location_mapping = location_data.set_index('name_cleaned')['id'].to_dict()

    # Map asset IDs
    space_data['asset*'] = space_data['asset_name_cleaned'].map(location_mapping)

    # Clean up temporary column
    space_data.drop(columns=['asset_name_cleaned'], inplace=True)
    
    logger.info(f"Mapped {len(space_data[space_data['asset*'].notna()])} asset IDs")
    return space_data
