import os
import sys
import pandas as pd

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.error_handler import handle_error, logger
from utils.helpers import get_short_form

@handle_error
def generate_asset_ids(df):
    """Generate asset IDs for the given DataFrame"""
    required_cols = ["Building", "Location", "Space", "Subspace", 
                    "Asset System", "Asset / Equipment"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    
    asset_counts = {}
    df["Asset ID"] = df.apply(
        lambda row: generate_single_asset_id(row, asset_counts), 
        axis=1
    )
    
    logger.info(f"Generated {len(df)} asset IDs")
    return df

def generate_single_asset_id(row, asset_counts):
    """Generate a single asset ID"""
    components = [
        get_short_form(row['Building']),
        get_short_form(row['Location']),
        get_short_form(row['Space']),
        get_short_form(row['Subspace'])
    ]
    
    eqp = ("UNK" if pd.isna(row['Asset / Equipment']) 
           else get_short_form(row['Asset / Equipment']))
    if eqp == "UNK" and not pd.isna(row['Asset System']):
        eqp = get_short_form(row['Asset System'])
    
    components.append(eqp)
    base_id = "-".join(components)
    
    if base_id not in asset_counts:
        asset_counts[base_id] = 1
    else:
        asset_counts[base_id] += 1
    return f"{base_id}-{asset_counts[base_id]}"
