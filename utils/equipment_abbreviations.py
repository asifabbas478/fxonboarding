"""Equipment abbreviation mappings and generator"""
import re
import os
import requests
from typing import Dict, Optional

# Common equipment abbreviations
EQUIPMENT_ABBR = {
    # HVAC Equipment
    'exhaust fan': 'EXF',
    'supply fan': 'SF',
    'air handling unit': 'AHU',
    'fan coil unit': 'FCU',
    'split ac': 'SAC',
    'package unit': 'PKU',
    'cooling tower': 'CT',
    'chiller': 'CHR',
    'ductless split unit': 'DSU',
    
    # Electrical Equipment
    'electrical lighting fixtures': 'ELF',
    'light fixture': 'LF',
    'distribution board': 'DB',
    'transformer': 'TRF',
    'ups': 'UPS',
    'generator': 'GEN',
    'water heater': 'WH',
    
    # Plumbing Equipment
    'plumbing accessories': 'PLB',
    'sanitary wares': 'SNW',
    'sanitary wares & fittings': 'SNW',
    'water pump': 'WP',
    'water tank': 'WT',
    
    # Fire Systems
    'fire alarm': 'FA',
    'fire extinguisher': 'FE',
    'sprinkler': 'SPK',
    
    # Building Systems
    'elevator': 'ELV',
    'escalator': 'ESC',
    'cctv': 'CCTV',
    'access control': 'ACC',
    
    # Asset Systems (used when equipment name is not available)
    'hvac': 'HVC',
    'electrical': 'ELE',
    'plumbing': 'PLB',
    'fire protection': 'FPS',
    'security': 'SEC',
    'appliances': 'APP',
    
    # Additional mappings
    'none': 'EQP',  # Default for empty/none values
}

def get_openai_abbreviation(equipment_name: str, max_length: int = 4) -> Optional[str]:
    """Get an abbreviation suggestion from OpenAI"""
    try:
        # Get API key from environment or secrets file
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            secrets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.streamlit', 'secrets.toml')
            if os.path.exists(secrets_path):
                with open(secrets_path, 'r') as f:
                    for line in f:
                        if line.startswith('openai_api_key'):
                            api_key = line.split('=')[1].strip().strip('"\'')
                            break
        
        if not api_key:
            return None
            
        # Call OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{
                    "role": "system",
                    "content": f"Create a meaningful {max_length}-letter abbreviation for equipment names. "
                              "The abbreviation should be intuitive and follow industry standards when possible. "
                              "Respond with ONLY the abbreviation in uppercase, nothing else."
                }, {
                    "role": "user",
                    "content": equipment_name
                }],
                "max_tokens": 10,
                "temperature": 0.3
            }
        )
        
        if response.status_code == 200:
            abbr = response.json()["choices"][0]["message"]["content"].strip()
            # Ensure it meets our requirements
            abbr = re.sub(r'[^A-Z]', '', abbr.upper())
            return abbr[:max_length] if abbr else None
            
    except Exception as e:
        print(f"Error getting AI abbreviation: {str(e)}")
    return None

def get_equipment_abbreviation(equipment_name: str, max_length: int = 4) -> str:
    """Get or generate an abbreviation for equipment name"""
    if not equipment_name or equipment_name.lower() == 'none':
        return 'EQP'
        
    # Clean and standardize the name
    clean_name = equipment_name.lower().strip()
    
    # Check predefined mappings
    if clean_name in EQUIPMENT_ABBR:
        return EQUIPMENT_ABBR[clean_name]
        
    # Try AI-generated abbreviation
    ai_abbr = get_openai_abbreviation(clean_name, max_length)
    if ai_abbr:
        # Cache the result for future use
        EQUIPMENT_ABBR[clean_name] = ai_abbr
        return ai_abbr
        
    # Fallback: take first letter of each word
    words = clean_name.split()
    if len(words) > 1:
        abbr = ''.join(word[0] for word in words if word)
        return abbr[:max_length].upper() if abbr else 'EQP'
    
    # Single word: take first max_length characters
    return clean_name[:max_length].upper() if clean_name else 'EQP'
