import os
import json
from openai import OpenAI

def plan_task(task: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = (
        f"You are a task planner. Break down the following task into a JSON list of ordered, "
        f"actionable steps. Return ONLY the JSON array, with no markdown formatting or extra text.\n\n"
        f"Task: {task}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return json.loads(response.choices[0].message.content.strip())
