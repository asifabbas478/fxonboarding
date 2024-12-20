# Facilitrol-X Onboarding Assistant

A Streamlit-based application for managing and processing asset data in the Facilitrol-X system.

## Project Structure

```
facilitrol_x_onboarding/
├── utils/                  # Utility functions and error handling
│   ├── error_handler.py    # Error handling and logging
│   └── helpers.py         # Helper functions
├── processors/            # Data processing modules
│   ├── asset_id_processor.py
│   ├── facility_processor.py
│   ├── location_processor.py
│   ├── space_processor.py
│   ├── equipment_processor.py
│   └── system_asset_processor.py
├── ui/                    # User interface components
│   └── pages.py          # Page rendering functions
├── app.py                # Main application file
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Features

- Asset ID Generation
- Facility Data Processing
- Location Data Processing
- Space Data Processing
- Equipment Data Processing
- System Asset ID Mapping

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the following command from the project directory:
```bash
streamlit run app.py
```

## Usage

1. Select the desired process from the sidebar
2. Upload the required files
3. Enter the namespace (if required)
4. Process the data
5. Download the processed files

## Error Handling

The application includes comprehensive error handling and logging:
- All errors are logged to both console and file
- User-friendly error messages are displayed in the UI
- Each processing function includes validation checks
