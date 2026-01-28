import google.generativeai as genai
from utils import KeyManager
import time
from google.api_core import exceptions

key_manager = KeyManager()
key_manager.configure_genai()

def generate_content_with_retry(model, prompt):
    max_retries = len(key_manager.api_keys) * 2 # Try through all keys twice
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response
        except exceptions.ResourceExhausted as e:
            print(f"Quota exceeded on key index {key_manager.current_key_index}. Rotating key...")
            key_manager.rotate_key()
            key_manager.configure_genai()
            time.sleep(1) # Short cool-off
        except Exception as e:
             # For other exceptions, re-raise immediately
            print(f"An error occurred: {e}")
            raise e
    
    raise Exception("All API keys exhausted or failed.")

# Helper to get model, ensuring configuration is current
def get_model(model_name="gemini-pro"):
    return genai.GenerativeModel(model_name)

