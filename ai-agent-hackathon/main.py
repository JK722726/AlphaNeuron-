import sys
import re
import agent
import tools

def main():
    print("AI Agent CLI")
    print("------------")
    
    # 1. Read User Input
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        try:
            task = input("Enter your task: ")
        except EOFError:
            return

    if not task:
        print("No task provided. Exiting.")
        return

    # 2. Call Planner
    print(f"\n[PLANNER] Generating plan for: '{task}'...")
    try:
        plan = agent.plan_task(task)
        print(f"[PLANNER] Plan generated: {len(plan)} steps.")
        for i, step in enumerate(plan):
            print(f"  {i+1}. {step}")
    except Exception as e:
        print(f"[ERROR] Planning failed: {e}")
        return

    # 3. Execute Steps
    context = "" # context to pass data between steps (e.g. search result -> summary)
    
    for i, step in enumerate(plan):
        print(f"\n[EXEC] Step {i+1}: {step}")
        
        # Determine intent and tool
        step_lower = str(step).lower()
        
        try:
            if "search" in step_lower:
                # Naive: use the whole step string as query if no context, or simple cleanup
                # Better: Remove "search for" etc.
                query = step  # Default
                # If we have regex skills, clean it up
                # But simple is robust. Let's send the step text.
                # Actually, searching for "Step 1: Search for apple" usually works ok in Google.
                
                result_map = tools.search_web(query)
                if result_map["status"] == "success":
                    print(f"[TOOL: SEARCH] Success.")
                    context = result_map["output"] # Update context with search results
                else:
                    print(f"[TOOL: SEARCH] Failed: {result_map['output']}")
                    print("[EXEC] Critical step failed. Stopping execution.")
                    break
                    
            elif "summarize" in step_lower:
                # Summarize the current context
                if not context:
                    print("[WARN] No content to summarize. Skipping.")
                    continue
                    
                result_map = tools.summarize_content(context)
                if result_map["status"] == "success":
                    print(f"[TOOL: SUMMARIZE] Success.")
                    context = result_map["output"] # Update context with summary
                else:
                    print(f"[TOOL: SUMMARIZE] Failed: {result_map['output']}")
                    print("[EXEC] Critical step failed. Stopping execution.")
                    break
            
            elif any(kw in step_lower for kw in ["write", "save", "create file"]):
                # Extract filename
                # Look for something that looks like a filename? or just ask user?
                # User constraint: "No UI".
                # Regex for filename
                match = re.search(r'[\w-]+\.\w+', step)
                filename = match.group(0) if match else "output.txt"
                
                result_map = tools.write_to_file(filename, context)
                if result_map["status"] == "success":
                    print(f"[TOOL: WRITE] Saved to {filename}")
                else:
                    print(f"[TOOL: WRITE] Failed: {result_map['output']}")
            
            else:
                print(f"[EXEC] No matching tool found for step. Skipping execution.")
                
        except Exception as e:
            print(f"[ERROR] Step execution failed: {e}")

    print("\n[DONE] Execution complete.")

if __name__ == "__main__":
    main()
