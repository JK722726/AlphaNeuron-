# AI Agent Hackathon Project

A single-agent system that plans and executes tasks using Google Gemini and SerpApi.

## Structure
- `agent.py`: Planner using Gemini Pro/Flash to break tasks into JSON steps.
- `tools.py`: Toolset including Web Search (SerpApi), Summarization (Gemini), and File Writing.
- `main.py`: CLI execution loop that orchestrates the agent.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up `.env` file with:
   - `GOOGLE_API_KEY_1`
   - `SERPAPI_API_KEY`
   - `GEMINI_MODEL` (optional, defaults to `gemini-2.5-flash`)

## Usage
Run the agent with a task string:
```bash
python main.py "Research the history of AI and summarize it to a file called ai_history.txt"
```

## Features
- **Strict JSON Planning**: Uses Gemini to ensure robust planning.
- **Reliable Execution**: Stops gracefully if critical tools fail.
- **Context Passing**: Passes output from one tool (e.g., search results) to the next (e.g., summarizer).
