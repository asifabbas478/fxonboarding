"""Service for generating abbreviations using AI"""
import re
import os
import requests
from typing import Dict, Optional

# Common abbreviation mappings
COMMON_ABBR = {
    # Locations
    'compound management office': 'CMO',
    'management office': 'MGO',
    'food court': 'FC',
    'ladies gym area': 'LGA',
    'gents gym area': 'GGA',
    'gameplay area': 'GPA',
    'kids play area': 'KPA',
    'cafeteria': 'CAF',
    'display area': 'DSP',
    
    # Equipment
    'exhaust fan': 'EXF',
    'supply fan': 'SF',
    'air handling unit': 'AHU',
    'fan coil unit': 'FCU',
    'split ac': 'SAC',
    'package unit': 'PKU',
    'cooling tower': 'CT',
    'water heater': 'WH',
    'distribution board': 'DB',
    
    # Systems
    'hvac': 'HVC',
    'electrical': 'ELE',
    'plumbing': 'PLB',
    'fire protection': 'FPS',
    'security': 'SEC',
}

def get_ai_abbreviation(text: str, max_length: int = 4, system_prompt: str = None) -> Optional[str]:
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
            
        if not system_prompt:
            system_prompt = (f"Create a meaningful {max_length}-letter abbreviation that is intuitive "
                           "and follows industry standards when possible. "
                           "Respond with ONLY the abbreviation in uppercase, nothing else.")
            
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
                    "content": system_prompt
                }, {
                    "role": "user",
                    "content": text
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

def get_abbreviation(text: str, max_length: int = 4, type_hint: str = None) -> str:
    """Get or generate an abbreviation for any text"""
    if not text or text.lower() == 'none':
        return 'NA'
        
    # Clean and standardize the text
    clean_text = text.lower().strip()
    
    # Check predefined mappings
    if clean_text in COMMON_ABBR:
        return COMMON_ABBR[clean_text]
    
    # Prepare system prompt based on type
    system_prompt = None
    if type_hint == 'location':
        system_prompt = (f"Create a {max_length}-letter abbreviation for a building location or area name. "
                        "Make it intuitive and memorable. Response should be ONLY the abbreviation in uppercase.")
    elif type_hint == 'equipment':
        system_prompt = (f"Create a {max_length}-letter abbreviation for facility equipment or system. "
                        "Use industry standard abbreviations where possible. Response should be ONLY the abbreviation in uppercase.")
        
    # Try AI-generated abbreviation
    ai_abbr = get_ai_abbreviation(clean_text, max_length, system_prompt)
    if ai_abbr:
        # Cache the result for future use
        COMMON_ABBR[clean_text] = ai_abbr
        return ai_abbr
        
    # Fallback: take first letter of each word
    words = clean_text.split()
    if len(words) > 1:
        abbr = ''.join(word[0] for word in words if word)
        return abbr[:max_length].upper() if abbr else 'NA'
    
    # Single word: take first max_length characters
    return clean_text[:max_length].upper() if clean_text else 'NA'
