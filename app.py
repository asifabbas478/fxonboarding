import os
import sys
import streamlit as st
from pathlib import Path

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from ui.pages import (
    render_asset_id_page,
    render_facility_page,
    render_location_page,
    render_space_page,
    render_equipment_page,
    render_system_asset_page
)

def main():
    st.set_page_config(page_title="Facilitrol-X Onboarding Assistant", layout="wide")
    st.title("Facilitrol-X Onboarding Assistant")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Select Process",
        ["Asset ID Generator", "Facility Processing", "Location Processing", 
         "Space Processing", "Equipment Processing", "System Asset ID Mapping"]
    )
    
    # Common inputs
    namespace = st.sidebar.text_input("Namespace*", help="Required for all operations")
    
    # Render the selected page
    if page == "Asset ID Generator":
        render_asset_id_page()
    elif page == "Facility Processing":
        render_facility_page(namespace)
    elif page == "Location Processing":
        render_location_page(namespace)
    elif page == "Space Processing":
        render_space_page(namespace)
    elif page == "Equipment Processing":
        render_equipment_page(namespace)
    elif page == "System Asset ID Mapping":
        render_system_asset_page()

if __name__ == "__main__":
    main()
