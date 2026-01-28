import os
import requests
import utils

def log_tool_usage(tool_name: str):
    print(f"[TOOL] Executing: {tool_name}")

def search_web(query: str):
    """
    Searches the web using SerpApi.
    Returns: {"status": "success"|"error", "output": str}
    """
    log_tool_usage("search_web")
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        return {"status": "error", "output": "SERPAPI_API_KEY not found."}
    
    try:
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google"
        }
        response = requests.get("https://serpapi.com/search", params=params, timeout=15)
        response.raise_for_status()
        results = response.json()
        
        organic_results = results.get("organic_results", [])
        if not organic_results:
            return {"status": "success", "output": "No results found."}
            
        snippets = [r.get("snippet", "") for r in organic_results[:3]]
        return {"status": "success", "output": "\n".join(snippets)}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
             return {"status": "error", "output": "SerpApi rate limit exceeded."}
        return {"status": "error", "output": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "output": f"Search failed: {str(e)}"}

def summarize_content(content: str):
    """
    Summarizes content using Gemini with key rotation.
    Returns: {"status": "success"|"error", "output": str}
    """
    log_tool_usage("summarize_content")
    
    # Cap input length
    max_len = 10000
    if len(content) > max_len:
        content = content[:max_len] + "...(truncated)"
    
    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    
    try:
        prompt = f"Summarize the following content concisely:\n\n{content}"
        output = utils.generate_content_with_retry(model_name, prompt)
        return {"status": "success", "output": output.strip()}
    except Exception as e:
        return {"status": "error", "output": f"Summarization failed: {str(e)}"}

def write_to_file(filename: str, content: str):
    """
    Writes content to a file.
    Returns: {"status": "success"|"error", "output": str}
    """
    log_tool_usage("write_to_file")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"status": "success", "output": f"Successfully wrote to {filename}"}
    except Exception as e:
        return {"status": "error", "output": f"File write failed: {str(e)}"}
