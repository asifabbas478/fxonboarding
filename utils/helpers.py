import pandas as pd

def get_short_form(text):
    """Get short form of text for asset ID generation"""
    if pd.isna(text) or str(text).strip() == "":
        return "UNK"
    text = str(text).strip()
    return text[:3].upper() if len(text) >= 3 else text.upper()

def clean_and_truncate_facility_name(name, substrings_to_ignore):
    """Clean and truncate facility names"""
    if isinstance(name, str):
        for substring in substrings_to_ignore:
            name = name.replace(substring, "")
        return name.split(",")[0].strip()
    return name
