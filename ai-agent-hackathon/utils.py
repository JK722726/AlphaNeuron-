import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Global state for current key index
_current_key_index = 0
_keys = []

def _load_keys():
    global _keys
    _keys = []
    i = 1
    while True:
        key = os.environ.get(f"GOOGLE_API_KEY_{i}")
        if not key:
            break
        _keys.append(key)
        i += 1
    
    if not _keys:
        raise ValueError("No GOOGLE_API_KEYs (GOOGLE_API_KEY_1, etc.) found in environment.")

def _get_current_key():
    global _current_key_index, _keys
    if not _keys:
        _load_keys()
    return _keys[_current_key_index]

def _rotate_key():
    global _current_key_index, _keys
    _current_key_index = (_current_key_index + 1) % len(_keys)
    print(f"[SYSTEM] Rotating API Key to index {_current_key_index + 1}")

def generate_content_with_retry(model_name: str, prompt: str, temperature: float = 0.0):
    """
    Generates content using Gemini with automatic API key rotation on quota/permission errors.
    """
    # Ensure keys are loaded
    if not _keys:
        _load_keys()
        
    attempts = 0
    max_attempts = len(_keys)
    
    while attempts < max_attempts:
        current_key = _get_current_key()
        
        try:
            genai.configure(api_key=current_key)
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            # Check for typical exhaustion/auth errors: 429, 403, 400 (sometimes check quota)
            # We catch broadly if it looks like an API issue that rotation might fix
            is_auth_error = "403" in error_str or "API key" in error_str
            is_quota_error = "429" in error_str or "Quota" in error_str or "ResourceExhausted" in error_str
            
            if is_auth_error or is_quota_error:
                print(f"[WARN] API Key {_current_key_index + 1} failed: {error_str.splitlines()[0]}... Rotating.")
                _rotate_key()
                attempts += 1
                time.sleep(1) # Brief cool-off
            else:
                # Fatal error (e.g. bad request, parsing), re-raise
                raise e
                
    raise RuntimeError("All available API keys have been exhausted or failed.")
