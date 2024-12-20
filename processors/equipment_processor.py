import os
import sys
import pandas as pd
from io import StringIO

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.error_handler import handle_error, logger
from utils.validation_constants import EQUIPMENT_TYPES, EQUIPMENT_CLASSES

def validate_equipment_data(df, source_data):
    """Validate equipment types and classes in the dataframe"""
    warnings = []
    
    # Convert sets to case-insensitive for comparison
    valid_types = {t.lower().strip() for t in EQUIPMENT_TYPES}
    valid_classes = {c.lower().strip() for c in EQUIPMENT_CLASSES}
    
    # Track unique non-standard values for summary
    non_standard_classes = set()
    non_standard_types = set()
    
    # Check equipment class (Asset System)
    for idx, row in source_data.iterrows():
        asset_system = row['Asset System']
        if pd.notna(asset_system) and asset_system != 'Mandatory':
            if asset_system.lower().strip() not in valid_classes:
                warnings.append(f"Row {idx + 2}: Non-standard equipment class '{asset_system}' in Asset System column")
                non_standard_classes.add(asset_system)
    
    # Check equipment type (Asset / Equipment)
    for idx, row in source_data.iterrows():
        asset_equipment = row['Asset / Equipment']
        if pd.notna(asset_equipment) and asset_equipment != 'Mandatory':
            if asset_equipment.lower().strip() not in valid_types:
                warnings.append(f"Row {idx + 2}: Non-standard equipment type '{asset_equipment}' in Asset/Equipment column")
                non_standard_types.add(asset_equipment)
    
    if warnings:
        # Add summary of unique non-standard values
        summary = []
        if non_standard_classes:
            summary.extend([
                "\nNon-standard Equipment Classes found:",
                "================================",
                *[f"- {cls}" for cls in sorted(non_standard_classes)]
            ])
        if non_standard_types:
            summary.extend([
                "\nNon-standard Equipment Types found:",
                "================================",
                *[f"- {typ}" for typ in sorted(non_standard_types)]
            ])
        warnings.extend(summary)
        
        warnings.append("\nNote: You can proceed with the upload, but make sure to create these equipment classes/types in your system.")
    
    return warnings

@handle_error
def process_equipment_data(asset_location_file, equipment_template, namespace):
    """Process equipment data"""
    logger.info("Starting equipment data processing")
    
    # Load data
    asset_location_data = pd.read_excel(asset_location_file, sheet_name='Asset,location')
    template_data = pd.read_csv(equipment_template)
    
    # Extract unique equipment data
    unique_data = asset_location_data[
        ['Barcode', 'Asset System', 'Asset / Equipment', 'Asset Criticality', 'Sublocation']
    ].drop_duplicates()
    
    # Filter valid data
    valid_data = unique_data[
        (unique_data['Asset System'].notna() | unique_data['Asset / Equipment'].notna()) &
        (unique_data['Asset System'] != 'Mandatory') &
        (unique_data['Asset / Equipment'] != 'Mandatory')
    ]
    
    # Check for non-standard equipment data
    validation_warnings = validate_equipment_data(template_data, valid_data)
    
    # Create new equipment data
    new_equipment_data = pd.DataFrame({
        'barcode': valid_data['Barcode'].reset_index(drop=True),
        'name*': valid_data.apply(
            lambda x: x['Asset / Equipment'] if pd.notna(x['Asset / Equipment']) else x['Asset System'],
            axis=1
        ).reset_index(drop=True),
        'type': valid_data['Asset / Equipment'].reset_index(drop=True),  # Equipment Type
        'class': valid_data['Asset System'].reset_index(drop=True),      # Equipment Class
        'criticality': valid_data['Asset Criticality'].reset_index(drop=True),
        'space name': valid_data['Sublocation'].reset_index(drop=True),
        'namespace*': namespace,
        'isActive*': True
    })
    
    # Merge with template
    template_data_cleaned = template_data.iloc[1:]
    updated_equipment_data = pd.concat([template_data_cleaned, new_equipment_data], ignore_index=True)
    
    # If there are warnings, create a warning log
    warning_file = None
    if validation_warnings:
        warning_log = "\n".join([
            "Equipment Validation Warnings:",
            "==========================",
            *validation_warnings
        ])
        
        warning_file = StringIO()
        warning_file.write(warning_log)
        warning_file.seek(0)
        
        logger.warning(f"Found {len(validation_warnings)} non-standard equipment types/classes")
    
    logger.info(f"Processed {len(new_equipment_data)} equipment records successfully")
    return updated_equipment_data, warning_file
