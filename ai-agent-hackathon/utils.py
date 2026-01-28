import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class KeyManager:
    def __init__(self):
        self.api_keys = []
        # Load keys from environment
        i = 1
        while True:
            key = os.getenv(f"GOOGLE_API_KEY_{i}")
            if key:
                self.api_keys.append(key)
                i += 1
            else:
                break
        
        if not self.api_keys:
             # Fallback to single key if numbered keys are not found
            single_key = os.getenv("GOOGLE_API_KEY")
            if single_key:
                self.api_keys.append(single_key)

        if not self.api_keys:
            raise ValueError("No Google API keys found in environment variables.")

        self.current_key_index = 0
    
    def get_current_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"Switching to API Key index: {self.current_key_index}")
        return self.get_current_key()

    def configure_genai(self):
        genai.configure(api_key=self.get_current_key())
