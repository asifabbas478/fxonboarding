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
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    return os.path.join(template_dir, template_name)

def show_preview_table(df, title="Preview"):
    """Show a preview of the DataFrame with styling"""
    st.subheader(title)
    st.dataframe(
        df,
        hide_index=True,
        column_config={col: st.column_config.Column(
            width="medium"
        ) for col in df.columns}
    )

def render_asset_id_page():
    st.header("Asset ID Generator")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file:
        sheet_name = st.text_input("Enter sheet name", value="Asset,location")
        
        if st.button("Process File"):
            try:
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                result = generate_asset_ids(df)
                
                if result is not None:
                    show_preview_table(result, "Generated Asset IDs")
                    st.success("File processed successfully!")
                    
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
    
    # Upload facility file
    facility_file = st.file_uploader("Upload Facility File (Excel)", type=['xlsx'])
    
    if facility_file is not None:
        # Get template path
        template_path = get_template_path('facility_template.csv')
        
        if namespace:
            # Process the data
            result_df = process_facility_data(facility_file, template_path, namespace)
            
            if result_df is not None:
                # Show preview
                show_preview_table(result_df, "Processed Facility Data")
                
                # Download button
                output = io.BytesIO()
                result_df.to_csv(output, index=False)
                st.download_button(
                    label="Download Processed File",
                    data=output.getvalue(),
                    file_name="processed_facility.csv",
                    mime="text/csv"
                )

def render_location_page(namespace):
    st.header("Location Processing")
    
    location_file = st.file_uploader("Upload Location File (Excel)", type=['xlsx'])
    
    if location_file is not None:
        template_path = get_template_path('location_template.csv')
        
        if namespace:
            result_df = process_location_data(location_file, template_path, namespace)
            
            if result_df is not None:
                show_preview_table(result_df, "Processed Location Data")
                
                output = io.BytesIO()
                result_df.to_csv(output, index=False)
                st.download_button(
                    label="Download Processed File",
                    data=output.getvalue(),
                    file_name="processed_location.csv",
                    mime="text/csv"
                )

def render_space_page(namespace):
    st.header("Space Processing")
    
    space_file = st.file_uploader("Upload Space File (Excel)", type=['xlsx'])
    
    if space_file is not None:
        template_path = get_template_path('space_template.csv')
        
        if namespace:
            result_df = process_space_data(space_file, template_path, namespace)
            
            if result_df is not None:
                show_preview_table(result_df, "Processed Space Data")
                
                output = io.BytesIO()
                result_df.to_csv(output, index=False)
                st.download_button(
                    label="Download Processed File",
                    data=output.getvalue(),
                    file_name="processed_space.csv",
                    mime="text/csv"
                )

def render_equipment_page(namespace):
    st.header("Equipment Processing")
    
    equipment_file = st.file_uploader("Upload Equipment File (Excel)", type=['xlsx'])
    
    if equipment_file is not None:
        template_path = get_template_path('equipment_template.csv')
        
        if namespace:
            result = process_equipment_data(equipment_file, template_path, namespace)
            
            if isinstance(result, tuple):
                result_df, warning_file = result
                
                if warning_file:
                    st.warning("Found non-standard equipment types/classes. You can proceed, but please review the warning log.")
                    st.download_button(
                        label="Download Warning Log",
                        data=warning_file.getvalue(),
                        file_name="equipment_validation_warnings.txt",
                        mime="text/plain"
                    )
                
                show_preview_table(result_df, "Processed Equipment Data")
                
                output = io.BytesIO()
                result_df.to_csv(output, index=False)
                st.download_button(
                    label="Download Processed File",
                    data=output.getvalue(),
                    file_name="processed_equipment.csv",
                    mime="text/csv"
                )

def render_system_asset_page():
    st.header("System Asset ID Mapping")
    
    st.markdown("""
    ### Step 1: Upload Master Data File
    Upload a CSV file containing the master data with IDs that will be used for mapping.
    """)
    master_file = st.file_uploader("Upload Master Data File (CSV)", type=['csv'], key="master")
    
    if master_file:
        st.markdown("""
        ### Step 2: Upload File to Map
        Upload the CSV file that needs to be mapped against the master data IDs.
        """)
        target_file = st.file_uploader("Upload File to Map (CSV)", type=['csv'], key="target")
        
        if target_file:
            result_df = process_system_asset_mapping(master_file, target_file)
            
            if result_df is not None:
                show_preview_table(result_df, "ID Mapping Results")
                
                output = io.BytesIO()
                result_df.to_csv(output, index=False)
                st.download_button(
                    label="Download Mapped File",
                    data=output.getvalue(),
                    file_name="id_mapping_result.csv",
                    mime="text/csv"
                )
