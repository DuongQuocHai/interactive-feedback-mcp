#!/usr/bin/env python3
"""
Simple test client for the Interactive Feedback MCP server
"""
import json
import subprocess
import sys
import os

def test_mcp_server():
    """Test the MCP server by calling the interactive_feedback tool"""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "server_tkinter.py")
    
    # Prepare the MCP request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "interactive_feedback",
            "arguments": {
                "project_directory": "/Users/btk0092/Documents/mcp/interactive-feedback-mcp",
                "summary": "Test từ client - Bạn có thể thấy UI không?"
            }
        }
    }
    
    print("🚀 Starting MCP server test...")
    print(f"📁 Server path: {server_path}")
    print(f"📝 Request: {json.dumps(request, indent=2)}")
    print("\n" + "="*50)
    
    try:
        # Start the server process
        process = subprocess.Popen(
            ["uv", "run", "python", server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=script_dir
        )
        
        # Send the request
        request_json = json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=30)
        
        print("📤 Request sent!")
        print(f"📥 Response: {stdout}")
        if stderr:
            print(f"⚠️  Errors: {stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Request timed out - this is expected for interactive UI")
        process.kill()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if process.poll() is None:
            process.terminate()

if __name__ == "__main__":
    test_mcp_server()
