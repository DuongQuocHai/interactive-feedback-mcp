#!/usr/bin/env python3
"""
Direct test of the feedback UI without MCP protocol
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feedback_ui_tkinter import feedback_ui

def test_ui():
    """Test the feedback UI directly"""
    print("🚀 Testing feedback UI directly...")
    
    project_dir = "/Users/btk0092/Documents/mcp/interactive-feedback-mcp"
    prompt = "Test UI trực tiếp - Bạn có thể thấy cửa sổ này không?"
    
    print(f"📁 Project directory: {project_dir}")
    print(f"📝 Prompt: {prompt}")
    print("\n" + "="*50)
    print("🖥️  UI sẽ mở trong vài giây...")
    
    try:
        result = feedback_ui(project_dir, prompt)
        
        print("\n" + "="*50)
        print("✅ UI đã đóng!")
        print(f"📝 Feedback nhận được: {result['interactive_feedback']}")
        print(f"📋 Logs: {result['command_logs'][:200]}...")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ui()
