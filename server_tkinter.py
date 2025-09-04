# Interactive Feedback MCP (Tkinter Version)
# Developed by Fábio Ferreira (https://x.com/fabiomlferreira)
# Inspired by/related to dotcursorrules.com (https://dotcursorrules.com/)
import os
import sys
import json
import tempfile
import subprocess

from typing import Annotated, Dict

from fastmcp import FastMCP
from pydantic import Field

# The log_level is necessary for Cline to work: https://github.com/jlowin/fastmcp/issues/81
mcp = FastMCP("Interactive Feedback MCP", log_level="ERROR")

def launch_feedback_ui(project_directory: str, summary: str) -> dict[str, str]:
    # Create a temporary file for the feedback result
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_file = tmp.name

    try:
        # Get the path to feedback_ui_tkinter.py relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        feedback_ui_path = os.path.join(script_dir, "feedback_ui_tkinter.py")
        fallback_ui_path = os.path.join(script_dir, "feedback_ui_fallback.py")

        # Try tkinter UI first
        try:
            # Use system Python for tkinter to avoid Tcl/Tk issues
            import shutil
            system_python = shutil.which("python3")
            if not system_python:
                system_python = "/usr/bin/python3"
            
            args = [
                system_python,
                "-u",
                feedback_ui_path,
                "--project-directory", project_directory,
                "--prompt", summary,
                "--output-file", output_file
            ]
            
            # Set environment variables for Tcl/Tk
            env = os.environ.copy()
            # Try to find the correct Tcl/Tk version
            import platform
            if platform.system() == "Darwin":  # macOS
                # Try different Tcl/Tk versions
                possible_tcl_paths = [
                    '/System/Library/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts',
                    '/System/Library/Frameworks/Tcl.framework/Versions/8.5/Resources/Scripts',
                    '/usr/local/lib/tcl8.6',
                    '/opt/homebrew/lib/tcl8.6'
                ]
                possible_tk_paths = [
                    '/System/Library/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts',
                    '/System/Library/Frameworks/Tk.framework/Versions/8.5/Resources/Scripts',
                    '/usr/local/lib/tk8.6',
                    '/opt/homebrew/lib/tk8.6'
                ]
                
                # Find working paths
                for tcl_path in possible_tcl_paths:
                    if os.path.exists(tcl_path):
                        env['TCL_LIBRARY'] = tcl_path
                        break
                for tk_path in possible_tk_paths:
                    if os.path.exists(tk_path):
                        env['TK_LIBRARY'] = tk_path
                        break
            
            result = subprocess.run(
                args,
                check=False,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                close_fds=True,
                text=True,
                env=env
            )
            
            if result.returncode == 0:
                # Success with tkinter UI
                with open(output_file, 'r') as f:
                    result_data = json.load(f)
                os.unlink(output_file)
                return result_data
            else:
                # Tkinter failed, try fallback
                print(f"Tkinter UI failed (code {result.returncode}), trying fallback...")
                if result.stderr and "TclError" in result.stderr:
                    print("Tcl/Tk error detected, using fallback UI")
                else:
                    print(f"Unknown error: {result.stderr}")
                
        except Exception as e:
            print(f"Tkinter UI error: {e}, trying fallback...")
        
        # Fallback to text-based UI
        args = [
            sys.executable,
            "-u",
            fallback_ui_path,
            "--project-directory", project_directory,
            "--prompt", summary,
            "--output-file", output_file
        ]
        
        result = subprocess.run(
            args,
            check=False,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = f"Failed to launch feedback UI (both tkinter and fallback): {result.returncode}"
            if result.stderr:
                error_msg += f"\nSTDERR: {result.stderr}"
            if result.stdout:
                error_msg += f"\nSTDOUT: {result.stdout}"
            raise Exception(error_msg)

        # Read the result from the temporary file
        with open(output_file, 'r') as f:
            result_data = json.load(f)
        os.unlink(output_file)
        return result_data
        
    except Exception as e:
        if os.path.exists(output_file):
            os.unlink(output_file)
        raise e

def first_line(text: str) -> str:
    return text.split("\n")[0].strip()

@mcp.tool()
def interactive_feedback(
    project_directory: Annotated[str, Field(description="Full path to the project directory")],
    summary: Annotated[str, Field(description="Short, one-line summary of the changes")],
) -> Dict[str, str]:
    """Request interactive feedback for a given project directory and summary"""
    return launch_feedback_ui(first_line(project_directory), first_line(summary))

if __name__ == "__main__":
    mcp.run(transport="stdio")
