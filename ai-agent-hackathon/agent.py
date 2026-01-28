import json
import os
import utils

def plan_task(task: str):
    """
    converts a user task into an ordered list of actionable steps.
    Uses Gemini with automatic retry and API-key fallback.
    Input: task (natural language string)
    Output: Python list of step strings (ordered)
    """
    model_name = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
    
    prompt = f"""You are an autonomous agent planner.
Your goal is to convert the following user task into a sequential list of actionable steps.

Available Capabilities:
1. Web Search (gather information)
2. Summarization (condense information)
3. File Writing (save outputs)

Rules:
- The output MUST be a strict JSON array of strings.
- Each string must be a clear, high-level instruction.
- Do NOT use specific tool names or code.
- Do NOT include any text outside the JSON array.
- The steps should be logical and sufficient to complete the task.

User Task: {task}

Example Output:
[
    "Search for the latest news on AI agents",
    "Summarize the key findings from the search results",
    "Write the summary to a file named agent_report.txt"
]
"""

    try:
        response = utils.generate_content_with_retry(model_name, prompt, temperature=0.0)
        
        # rudimentary cleanup for markdown code blocks
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        elif clean_response.startswith("```"):
            clean_response = clean_response[3:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
            
        steps = json.loads(clean_response.strip())
        
        if not isinstance(steps, list):
            raise ValueError("Output must be a list of steps")
            
        return steps

    except Exception as e:
        raise RuntimeError(f"Planning failed: {str(e)}")
