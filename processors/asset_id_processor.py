"""Asset ID generation processor"""
from typing import Dict, Optional, List
import re
import streamlit as st
import pandas as pd
from collections import defaultdict
from utils.column_mapping import validate_columns, apply_column_mapping, clean_text_for_id
from utils.abbreviation_service import get_abbreviation

def _clean_id_part(text: str) -> str:
    """Clean and standardize ID part"""
    if not text:
        return ''
    # Remove spaces and special characters, convert to uppercase
    cleaned = ''.join(c for c in str(text).strip() if c.isalnum() or c == ' ')
    # Replace remaining spaces with nothing
    cleaned = cleaned.replace(' ', '')
    return cleaned.upper()

def _abbreviate_building(name: str, max_len: int = 4) -> str:
    """Create an abbreviation for building name"""
    if not name:
        return ''
    return get_abbreviation(name, max_len, 'location')

def _get_equipment_code(row: pd.Series) -> str:
    """Get equipment code based on Asset/Equipment or Asset System"""
    # First try Asset/Equipment
    equipment = str(row.get('Asset / Equipment', '')).strip()
    if equipment and equipment.lower() != 'none':
        return get_abbreviation(equipment, 4, 'equipment')
    
    # If no equipment, try Asset System
    system = str(row.get('Asset System', '')).strip()
    if system and system.lower() != 'none':
        return get_abbreviation(system, 4, 'equipment')
    
    return 'EQP'  # Default if no valid value found

def _get_location_code(text: str, max_len: int = 4) -> str:
    """Get abbreviated location code"""
    if not text:
        return ''
    return get_abbreviation(text, max_len, 'location')

def generate_location_id(row: pd.Series, enabled: bool) -> str:
    """Generate location ID from Building and Floor"""
    if not enabled:
        return ''
        
    building = str(row.get('Building', '')).strip()
    floor = _clean_id_part(str(row.get('Floor', '')).strip())
    
    if not building or not floor:
        return ''
    
    building_code = _abbreviate_building(building)
    
    return f"{building_code}-{floor}"

def generate_space_id(row: pd.Series, enabled: bool) -> str:
    """Generate space ID from Building, Floor, and Sublocation"""
    if not enabled:
        return ''
        
    location_id = generate_location_id(row, True)
    sublocation = str(row.get('Sublocation', '')).strip()
    
    if not location_id or not sublocation:
        return ''
    
    # Get abbreviated sublocation code
    subloc_code = _get_location_code(sublocation)
    
    return f"{location_id}-{subloc_code}"

def generate_subspace_id(row: pd.Series, enabled: bool) -> str:
    """Generate subspace ID from Building, Floor, Sublocation, and Subspace"""
    if not enabled:
        return ''
        
    space_id = generate_space_id(row, True)
    subspace = str(row.get('Subspace', '')).strip()
    
    if not space_id or not subspace:
        return ''
    
    # Get abbreviated subspace code
    subspace_code = _get_location_code(subspace)
    
    return f"{space_id}-{subspace_code}"

def generate_equipment_id(row: pd.Series, counters: defaultdict, enabled: bool) -> str:
    """Generate equipment ID with full hierarchy and smart numbering"""
    if not enabled:
        return ''
    
    # Get all components with abbreviated codes
    location_id = generate_location_id(row, True)
    if not location_id:
        return ''
    
    sublocation = str(row.get('Sublocation', '')).strip()
    subloc_code = _get_location_code(sublocation) if sublocation else ''
    
    subspace = str(row.get('Subspace', '')).strip()
    subspace_code = _get_location_code(subspace) if subspace else ''
    
    # Get equipment code
    equipment_code = _get_equipment_code(row)
    
    # Create base ID without number
    base_id = f"{location_id}"
    if subloc_code:
        base_id += f"-{subloc_code}"
    if subspace_code:
        base_id += f"-{subspace_code}"
    base_id += f"-{equipment_code}"
    
    # Get counter for this combination
    counter = counters[base_id]
    counters[base_id] += 1
    
    return f"{base_id}-{counter}"

def generate_asset_ids(df: pd.DataFrame, settings: Dict[str, bool]) -> pd.DataFrame:
    """Main function to generate asset IDs for the dataframe."""
    try:
        # Convert all column names to strings
        df.columns = df.columns.astype(str)
        
        # Validate and map columns
        missing_columns, column_mapping = validate_columns(df, 'asset_id')
        
        if missing_columns:
            missing_cols_str = ', '.join(missing_columns)
            st.warning(f"Some columns are missing or renamed: {missing_cols_str}. Using column mapping to proceed.")
        
        # Apply column mapping if needed
        if column_mapping:
            df = apply_column_mapping(df, column_mapping)
        
        # Initialize counter dictionary for equipment IDs
        equipment_counters = defaultdict(lambda: 1)
        
        # Create a copy to avoid modifying the original
        result_df = df.copy()
        
        # Process each row
        for index, row in df.iterrows():
            # Generate IDs based on settings
            if settings['create_location_id']:
                result_df.at[index, 'location_id'] = generate_location_id(row, True)
                
            if settings['create_space_id']:
                result_df.at[index, 'space_id'] = generate_space_id(row, True)
                
            if settings['create_subspace_id']:
                result_df.at[index, 'subspace_id'] = generate_subspace_id(row, True)
                
            if settings['create_equipment_id']:
                result_df.at[index, 'equipment_id'] = generate_equipment_id(row, equipment_counters, True)
        
        return result_df
        
    except Exception as e:
        st.error(f"Error processing asset IDs: {str(e)}")
        raise e
