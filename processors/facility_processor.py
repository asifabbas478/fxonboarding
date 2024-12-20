import os
import sys
import pandas as pd

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.error_handler import handle_error, logger

@handle_error
def process_facility_data(facility_file, template_file, namespace):
    """Process facility data"""
    logger.info("Starting facility data processing")
    
    # Load the AFM file and the facility template
    afm_data = pd.read_excel(facility_file, sheet_name='Building (Facility)')
    facility_template_data = pd.read_csv(template_file)
    
    # Define the required column mappings
    required_columns = {
        "name*": "Building Name",
        "facilityType*": "Facility Type",
        "criticality": "Building Criticality",
        "location.longitude": "Longitude",
        "location.latitude": "Latitude",
    }
    
    # Validate required columns
    missing_cols = [col for col, mapped_col in required_columns.items() 
                   if mapped_col not in afm_data.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    
    # Normalize the criticality values
    afm_data["Building Criticality"] = afm_data["Building Criticality"].str.extract(r"(C\d)")
    
    # Prepare the new data
    facility_data = pd.DataFrame({
        "name*": afm_data[required_columns["name*"]],
        "facilityType*": afm_data[required_columns["facilityType*"]],
        "criticality": afm_data[required_columns["criticality"]],
        "location.longitude": pd.to_numeric(afm_data[required_columns["location.longitude"]], errors='coerce'),
        "location.latitude": pd.to_numeric(afm_data[required_columns["location.latitude"]], errors='coerce'),
        "isActive*": True,
        "namespace*": namespace,
    })
    
    # Clean and filter data
    valid_criticality_values = ["C1", "C2", "C3"]
    cleaned_facility_data = facility_data[
        (facility_data["name*"].notna()) &
        (~facility_data["name*"].str.contains("Mandatory|name", case=False, na=False)) &
        (~facility_data["facilityType*"].str.contains("Mandatory|facility type", case=False, na=False)) &
        (facility_data["criticality"].isin(valid_criticality_values))
    ]
    
    # Remove placeholder rows and merge
    facility_template_data = facility_template_data.drop(index=[0, 1], errors='ignore').reset_index(drop=True)
    updated_facility_data = pd.concat([facility_template_data, cleaned_facility_data], ignore_index=True)
    
    logger.info(f"Processed {len(cleaned_facility_data)} facility records")
    return updated_facility_data
