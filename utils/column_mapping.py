"""Column mapping utilities"""
import pandas as pd

# Required columns for asset ID generation
REQUIRED_COLUMNS = {
    'asset_id': {
        'Building': ['building', 'facility', 'site', 'property'],
        'Floor': ['floor', 'level', 'storey'],
        'Sublocation': ['sublocation', 'sub location', 'location', 'area', 'zone'],
        'Subspace': ['subspace', 'sub space', 'room', 'space'],
        'Location Criticality': ['location criticality', 'criticality', 'priority'],
        'Sublocation Criticality': ['sublocation criticality', 'space criticality'],
        'Subspace Criticality': ['subspace criticality', 'room criticality']
    }
}

def clean_text_for_id(text):
    """Clean and format text for ID generation"""
    if pd.isna(text) or text == '':
        return ''
    # Convert to string first
    text_str = str(text).strip()
    # Remove special characters and spaces, convert to uppercase
    cleaned = ''.join(c for c in text_str if c.isalnum() or c.isspace())
    # Convert spaces to underscores for subspace
    cleaned = cleaned.replace(' ', '_')
    return cleaned.upper()

def get_closest_match(column, possible_matches):
    """Find the closest matching standard column name"""
    try:
        # Convert column to string and handle numeric values
        column_str = str(column)
        column_lower = column_str.lower().strip()
        return column_lower in possible_matches
    except (AttributeError, TypeError):
        return False

def validate_columns(df, processor_type='asset_id'):
    """
    Validate if all required columns are present
    Returns:
    - missing_columns: list of required columns not found
    - column_mapping: dict of {standard_name: actual_column_name}
    """
    missing_columns = []
    column_mapping = {}
    
    # Convert all column names to strings and handle numeric columns
    df_columns = df.columns.astype(str)
    df_columns_lower = [col.lower().strip() for col in df_columns]

    for required_col, alternatives in REQUIRED_COLUMNS[processor_type].items():
        found = False
        for col in df_columns_lower:
            if col in alternatives:
                column_mapping[required_col] = df_columns[df_columns_lower.index(col)]
                found = True
                break
        if not found:
            missing_columns.append(required_col)

    return missing_columns, column_mapping

def apply_column_mapping(df, mapping):
    """Apply the column mapping to the dataframe"""
    df_copy = df.copy()
    for standard_name, actual_name in mapping.items():
        if actual_name in df.columns and actual_name != standard_name:
            df_copy[standard_name] = df[actual_name]
    return df_copy
