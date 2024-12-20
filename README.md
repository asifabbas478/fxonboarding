# Facilitrol-X Onboarding Assistant

A Streamlit-based application for generating standardized asset IDs and processing facility management data.

## Features

- Smart Asset ID Generation
  - Location IDs (FAC-LOC format)
  - Space IDs (FAC-LOC-SPC format)
  - Subspace IDs (FAC-LOC-SPC-SSP format)
  - Equipment IDs (FAC-LOC-SPC-SSP-EQP-X format)
- AI-Powered Equipment Abbreviation Generation
- Column Mapping for Flexible Data Import
- Excel File Processing
- Standardized Naming Conventions

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd facilitrol-x-onboarding
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up OpenAI API key:
Create a `.streamlit/secrets.toml` file with:
```toml
openai_api_key = "your-api-key"
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Select "Asset ID Generator" from the sidebar
2. Upload your Excel file
3. Enter the sheet name
4. Configure ID generation settings using the checkboxes
5. Click "Process File" to generate IDs
6. Download the processed file

## Equipment ID Generation

The system generates equipment IDs using the following logic:
1. Facility code from building name
2. Location from floor
3. Space from sublocation
4. Subspace from room/area
5. Equipment code from:
   - Asset/Equipment name (primary)
   - Asset System (fallback)
   - AI-generated abbreviation for unknown equipment

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- OpenAI API key (for AI-powered abbreviations)

## License

[Your chosen license]
