# Fallback UI for when tkinter is not available
# Simple text-based interface
import os
import sys
import json
import argparse
from typing import Optional, TypedDict

class FeedbackResult(TypedDict):
    command_logs: str
    interactive_feedback: str

def feedback_ui_fallback(project_directory: str, prompt: str, output_file: Optional[str] = None) -> Optional[FeedbackResult]:
    """Fallback UI when tkinter is not available"""
    print("=" * 60, file=sys.stderr)
    print("Interactive Feedback MCP - Fallback Mode", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"Project Directory: {project_directory}", file=sys.stderr)
    print(f"Summary: {prompt}", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # For server mode, provide a simple response without interactive input
    # This is a basic fallback that just returns the prompt as feedback
    command_logs = ""
    interactive_feedback = f"Fallback mode: {prompt}\n\nPlease use the tkinter UI for full functionality."
    
    result = FeedbackResult(
        logs=command_logs,
        interactive_feedback=interactive_feedback
    )
    
    if output_file:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f)
        return None
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fallback feedback UI")
    parser.add_argument("--project-directory", default=os.getcwd(), help="The project directory")
    parser.add_argument("--prompt", default="I implemented the changes you requested.", help="The prompt to show")
    parser.add_argument("--output-file", help="Path to save the feedback result as JSON")
    args = parser.parse_args()

    result = feedback_ui_fallback(args.project_directory, args.prompt, args.output_file)
    if result:
        print(f"\nLogs collected: \n{result['logs']}")
        print(f"\nFeedback received:\n{result['interactive_feedback']}")
    sys.exit(0)
