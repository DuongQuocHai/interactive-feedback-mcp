# Interactive Feedback MCP

Developed by Fábio Ferreira ([@fabiomlferreira](https://x.com/fabiomlferreira)).
Check out [dotcursorrules.com](https://dotcursorrules.com/) for more AI development enhancements.

Simple [MCP Server](https://modelcontextprotocol.io/) to enable a human-in-the-loop workflow in AI-assisted development tools like [Cursor](https://www.cursor.com). This server allows you to run commands, view their output, and provide textual feedback directly to the AI. It is also compatible with [Cline](https://cline.bot) and [Windsurf](https://windsurf.com).

## 🚀 Two Versions Available

### 🎯 **Tkinter Version (Recommended)**
- ✅ **100% Feature Parity** with PySide6 version
- ✅ **Cross-platform** (Windows, macOS, Linux)
- ✅ **No Dependencies** - uses built-in tkinter
- ✅ **Better Performance** and stability
- ✅ **Complete Settings Persistence**
- ✅ **Real-time Configuration Updates**

### 🔧 **PySide6 Version (Original)**
- Full-featured Qt-based UI
- Requires PySide6 installation
- Platform-specific dependencies

## ✨ Key Features

- **Interactive UI**: Modern, dark-themed interface
- **Command Execution**: Run commands directly in your project
- **Real-time Output**: See command results as they happen
- **Project-specific Settings**: Per-project configuration
- **Settings Persistence**: Cross-platform settings storage
- **Auto-execute**: Automatically run commands on startup
- **Keyboard Shortcuts**: Ctrl+Enter to submit feedback
- **External Links**: Clickable links in UI
- **Process Management**: Monitor and control running processes

## 💡 Why Use This?

By guiding the assistant to check in with the user instead of branching out into speculative, high-cost tool calls, this module can drastically reduce the number of premium requests (e.g., OpenAI tool invocations) on platforms like Cursor. In some cases, it helps consolidate what would be up to 25 tool calls into a single, feedback-aware request — saving resources and improving performance.

## 🎮 How It Works

1. **AI calls MCP** → UI appears
2. **View summary** from AI
3. **Run commands** (if needed) to test/verify
4. **Enter feedback** for AI
5. **Submit** → AI receives feedback and continues

## 📋 Installation (Cursor)

### Prerequisites
- Python 3.11 or newer
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DuongQuocHai/interactive-feedback-mcp.git
   cd interactive-feedback-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure in Cursor:**
   
   Add to your `mcp.json`:
   ```json
   {
     "mcpServers": {
       "interactive-feedback-mcp": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/interactive-feedback-mcp",
           "run",
           "server_tkinter.py"
         ],
         "timeout": 600,
         "autoApprove": ["interactive_feedback"]
       }
     }
   }
   ```

4. **Add Prompt Rule:**
   ```
   Whenever you want to ask a question, always call the MCP `interactive_feedback`.
   Whenever you're about to complete a user request, call the MCP `interactive_feedback` instead of simply ending the process. Keep calling MCP until the user's feedback is empty, then end the request.
   ```

## 🔧 Configuration

### Settings Storage
- **Tkinter Version**: JSON-based settings in platform-specific directories
- **PySide6 Version**: Qt's QSettings (registry/plist files)

### Project-specific Settings
- Command to run
- Auto-execute on startup
- Command section visibility
- Window geometry and state

## 🎯 Usage Examples

### Code Review
```
AI: "I've refactored calculateTotal(). Would you like to review?"
→ UI appears → Run tests → Enter feedback → Submit
AI: "Thanks! I'll fix the issues you mentioned."
```

### Feature Development
```
AI: "I've implemented login feature. Want to test?"
→ UI appears → Run "npm test" → Enter feedback → Submit
AI: "I'll improve based on your feedback."
```

## 🛠️ Development

### Test the UI directly:
```bash
uv run python test_ui_direct.py
```

### Run server in development mode:
```bash
uv run fastmcp dev server_tkinter.py
```

### Test MCP client:
```bash
uv run python test_client.py
```

## 📁 File Structure

```
interactive-feedback-mcp/
├── server_tkinter.py          # MCP Server (Tkinter - Recommended)
├── feedback_ui_tkinter.py     # UI (Tkinter)
├── settings_manager.py        # Settings Manager
├── server.py                  # MCP Server (PySide6 - Original)
├── feedback_ui.py             # UI (PySide6)
├── mcp.json                   # Cursor configuration template
├── COMPLETE_GUIDE.md          # Comprehensive usage guide
├── CURSOR_SETUP.md            # Cursor setup guide
└── test_*.py                  # Test files
```

## 🔍 Troubleshooting

### UI not showing:
```bash
# Test tkinter
uv run python -c "import tkinter; print('OK')"

# Test UI directly
uv run python test_ui_direct.py
```

### Server not running:
```bash
# Test server
uv run python server_tkinter.py

# Check logs
uv run fastmcp dev server_tkinter.py
```

## 📚 Documentation

- **[Complete Guide](COMPLETE_GUIDE.md)** - Comprehensive usage guide
- **[Cursor Setup](CURSOR_SETUP.md)** - Cursor configuration guide
- **[Feature Comparison](FEATURE_COMPARISON_UPDATED.md)** - Detailed feature analysis

## 🆚 Version Comparison

| Feature | PySide6 | Tkinter | Notes |
|---------|---------|---------|-------|
| **UI Components** | ✅ | ✅ | 100% equivalent |
| **Core Functionality** | ✅ | ✅ | 100% equivalent |
| **Settings Persistence** | ✅ | ✅ | 100% equivalent |
| **Cross-platform** | ⚠️ | ✅ | Tkinter better |
| **Dependencies** | ❌ | ✅ | Tkinter lighter |
| **Performance** | ✅ | ✅ | Equivalent |

## 🎉 Benefits

- **Save Time**: Less back-and-forth with AI
- **Reduce Costs**: Fewer premium requests
- **Improve Quality**: Direct, specific feedback
- **Increase Efficiency**: Smoother workflow

## Available Tools

Here's an example of how the AI assistant would call the `interactive_feedback` tool:

```xml
<use_mcp_tool>
  <server_name>interactive-feedback-mcp</server_name>
  <tool_name>interactive_feedback</tool_name>
  <arguments>
    {
      "project_directory": "/path/to/your/project",
      "summary": "I've implemented the changes you requested and refactored the main module."
    }
  </arguments>
</use_mcp_tool>
```

## Acknowledgements & Contact

If you find this Interactive Feedback MCP useful, the best way to show appreciation is by following Fábio Ferreira on [X @fabiomlferreira](https://x.com/fabiomlferreira).

For any questions, suggestions, or if you just want to share how you're using it, feel free to reach out on X!

Also, check out [dotcursorrules.com](https://dotcursorrules.com/) for more resources on enhancing your AI-assisted development workflow.

## License

MIT License - see [LICENSE](LICENSE) file for details.