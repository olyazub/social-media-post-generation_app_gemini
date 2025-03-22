import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # Required variables
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key is None:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        # Optional variables with defaults
        self.debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        
    @property
    def api_headers(self):
        return {
            'Authorization': f'Bearer {self.gemini_api_key}',
            'Content-Type': 'application/json'
        } 