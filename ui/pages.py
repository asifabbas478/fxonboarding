import os
import sys
import streamlit as st
import pandas as pd
import io

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from processors.asset_id_processor import generate_asset_ids
from processors.facility_processor import process_facility_data
from processors.location_processor import process_location_data
from processors.space_processor import process_space_data
from processors.equipment_processor import process_equipment_data
from processors.system_asset_processor import process_system_asset_mapping
from utils.error_handler import logger

def get_template_path(template_name):
    """Get the absolute path to a template file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', 'templates', template_name)

def show_preview_table(df, title="Preview"):
    """Show a preview of the DataFrame with styling"""
    st.subheader(title)
    st.dataframe(
        df,
        use_container_width=True,
        column_config={col: st.column_config.Column(
            width="medium"
        ) for col in df.columns}
    )

def render_asset_id_page():
    st.header("Asset ID Generator")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file:
        # Show ID generation options after file upload
        st.subheader("ID Generation Options")
        col1, col2 = st.columns(2)
        
        with col1:
            create_location_id = st.checkbox("Generate Location IDs (FAC-LOC-XXX)", value=False)
            create_space_id = st.checkbox("Generate Space IDs (FAC-LOC-SPC-XXX)", value=False)
            
        with col2:
            create_subspace_id = st.checkbox("Generate Subspace IDs (FAC-LOC-SPC-SSP-XXX)", value=False)
            create_equipment_id = st.checkbox("Generate Equipment IDs (EQP-XXX)", value=True)
        
        # Settings dictionary
        settings = {
            'create_location_id': create_location_id,
            'create_space_id': create_space_id,
            'create_subspace_id': create_subspace_id,
            'create_equipment_id': create_equipment_id
        }
        
        # Sheet name input
        sheet_name = st.text_input("Enter sheet name", value="Asset,location")
        
        # Process button
        if st.button("Process File"):
            try:
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                
                # Show preview of original data
                show_preview_table(df, "Original Data Preview")
                
                # Process the data with selected settings
                result = generate_asset_ids(df, settings)
                
                if result is not None:
                    show_preview_table(result, "Generated Asset IDs")
                    st.success("File processed successfully!")
                    
                    # Prepare download button
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result.to_excel(writer, index=False, sheet_name=sheet_name)
                    
                    st.download_button(
                        label="Download Processed Excel",
                        data=output.getvalue(),
                        file_name="processed_assets.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                st.error(f"Error processing file: {str(e)}")

def render_facility_page(namespace):
    st.header("Facility Processing")
    facility_file = st.file_uploader("Upload Facility File (Excel)", type=['xlsx'])
    if facility_file:
        try:
            template_file = "templates/facility_template.csv"
            result = process_facility_data(facility_file, template_file, namespace)
            if result is not None:
                show_preview_table(result)
                st.success("Facility file processed successfully!")
        except Exception as e:
            logger.error(f"Error processing facility file: {str(e)}")
            st.error(f"Error processing facility file: {str(e)}")

def render_location_page(namespace):
    st.header("Location Processing")
    location_file = st.file_uploader("Upload Location File (Excel)", type=['xlsx'])
    if location_file:
        try:
            result = process_location_data(location_file)
            if result is not None:
                show_preview_table(result)
                st.success("Location file processed successfully!")
        except Exception as e:
            logger.error(f"Error processing location file: {str(e)}")
            st.error(f"Error processing location file: {str(e)}")

def render_space_page(namespace):
    st.header("Space Processing")
    space_file = st.file_uploader("Upload Space File (Excel)", type=['xlsx'])
    if space_file:
        try:
            result = process_space_data(space_file)
            if result is not None:
                show_preview_table(result)
                st.success("Space file processed successfully!")
        except Exception as e:
            logger.error(f"Error processing space file: {str(e)}")
            st.error(f"Error processing space file: {str(e)}")

def render_equipment_page(namespace):
    st.header("Equipment Processing")
    equipment_file = st.file_uploader("Upload Equipment File (Excel)", type=['xlsx'])
    if equipment_file:
        try:
            result = process_equipment_data(equipment_file)
            if result is not None:
                show_preview_table(result)
                st.success("Equipment file processed successfully!")
        except Exception as e:
            logger.error(f"Error processing equipment file: {str(e)}")
            st.error(f"Error processing equipment file: {str(e)}")

def render_system_asset_page():
    st.header("System Asset Processing")
    system_asset_file = st.file_uploader("Upload System Asset File (Excel)", type=['xlsx'])
    if system_asset_file:
        try:
            result = process_system_asset_mapping(system_asset_file)
            if result is not None:
                show_preview_table(result)
                st.success("System asset file processed successfully!")
        except Exception as e:
            logger.error(f"Error processing system asset file: {str(e)}")
            st.error(f"Error processing system asset file: {str(e)}")
