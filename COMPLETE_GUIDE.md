# 🎯 Hướng dẫn hoàn chỉnh - Interactive Feedback MCP

## 🚀 Tổng quan

Interactive Feedback MCP (Tkinter Version) là phiên bản hoàn chỉnh với **100% tính năng** như bản gốc PySide6, được tối ưu cho cross-platform compatibility.

### 🎯 Mục đích
Interactive Feedback MCP cho phép AI (như Cursor) tương tác với bạn trong quá trình phát triển, giúp:
- **Giảm số lần gọi tool** (từ 25+ xuống 1 lần)
- **Tiết kiệm chi phí** premium requests
- **Cải thiện hiệu suất** AI development
- **Tương tác trực tiếp** với developer

## ✨ Tính năng đầy đủ

### 🎨 **UI Components**
- **Command Section**: Chạy commands trong project
- **Console Output**: Xem output real-time
- **Feedback Section**: Nhập feedback cho AI
- **Settings Panel**: Cấu hình project-specific
- **Toggle Controls**: Ẩn/hiện command section

### ⚙️ **Settings & Persistence**
- **Cross-platform Settings**: Windows, macOS, Linux
- **Project-specific Config**: Cấu hình riêng cho từng project
- **Window State Management**: Lưu vị trí và kích thước cửa sổ
- **Real-time Updates**: Cập nhật settings ngay lập tức
- **Auto-save**: Tự động lưu khi thay đổi

### 🔧 **Advanced Features**
- **Process Management**: Chạy và monitor commands
- **Keyboard Shortcuts**: Ctrl+Enter để submit
- **External Links**: Clickable links trong UI
- **Windows Path Formatting**: Format path cho Windows
- **Dark Theme**: Giao diện tối hiện đại

## 🔧 Cách hoạt động

### 1. AI gọi MCP `interactive_feedback`
Khi AI cần feedback từ bạn, nó sẽ gọi:
```json
{
  "tool": "interactive_feedback",
  "arguments": {
    "project_directory": "/path/to/your/project",
    "summary": "Tôi đã implement feature X, bạn có muốn test không?"
  }
}
```

### 2. UI hiển thị
Một cửa sổ UI sẽ xuất hiện với:
- **Feedback section**: Hiển thị summary từ AI
- **Command section**: Chạy commands trong project
- **Console**: Xem output của commands
- **Text input**: Nhập feedback cho AI

### 3. Bạn tương tác
- **Xem summary** từ AI
- **Chạy commands** để test (nếu cần)
- **Nhập feedback** cho AI
- **Submit** để gửi feedback

### 4. AI nhận feedback
AI nhận được:
```json
{
  "command_logs": "Output của commands bạn chạy",
  "interactive_feedback": "Feedback text bạn nhập"
}
```

## 📋 Cài đặt và cấu hình

### 1. **Cài đặt Dependencies**
```bash
cd /Users/btk0092/Documents/mcp/interactive-feedback-mcp
uv sync
```

### 2. **Cấu hình Cursor**

#### **File mcp.json:**
```json
{
  "mcpServers": {
    "interactive-feedback-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/btk0092/Documents/mcp/interactive-feedback-mcp",
        "run",
        "server_tkinter.py"
      ],
      "timeout": 600,
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

#### **Prompt Rule trong Cursor:**
```
Whenever you want to ask a question, always call the MCP `interactive_feedback`.
Whenever you're about to complete a user request, call the MCP `interactive_feedback` instead of simply ending the process. Keep calling MCP until the user's feedback is empty, then end the request.
```

### 3. **Khởi động Cursor**
- Restart Cursor
- Mở project bất kỳ
- Test với AI request

## 🎮 Cách sử dụng

### **Workflow cơ bản:**
1. **AI gọi MCP** → UI hiện
2. **Xem summary** từ AI
3. **Chạy commands** (nếu cần)
4. **Nhập feedback** cho AI
5. **Submit** → AI nhận feedback

### **Tính năng Command Section:**
- **Working Directory**: Hiển thị thư mục project
- **Command Input**: Nhập command để chạy
- **Run/Stop Button**: Chạy hoặc dừng command
- **Auto-execute**: Tự động chạy command khi mở UI
- **Save Config**: Lưu cấu hình cho project

### **Tính năng Console:**
- **Real-time Output**: Xem output của commands
- **Clear Button**: Xóa logs
- **Auto-scroll**: Tự động scroll xuống cuối
- **Process Status**: Hiển thị trạng thái process

### **Tính năng Feedback:**
- **Summary Display**: Hiển thị mô tả từ AI
- **Text Input**: Nhập feedback (Ctrl+Enter để submit)
- **Submit Button**: Gửi feedback cho AI

## 🚀 Workflow thực tế

### Ví dụ 1: Code Review
```
AI: "Tôi đã refactor function calculateTotal(). Bạn có muốn review không?"
→ UI hiện → Bạn chạy tests → Nhập feedback → Submit
AI: "Cảm ơn feedback! Tôi sẽ fix lỗi bạn chỉ ra."
```

### Ví dụ 2: Feature Development
```
AI: "Tôi đã implement login feature. Bạn muốn test không?"
→ UI hiện → Bạn chạy "npm test" → Nhập feedback → Submit
AI: "Tôi sẽ cải thiện theo feedback của bạn."
```

### Ví dụ 3: Bug Fix
```
AI: "Tôi đã fix bug trong API. Bạn có thể verify không?"
→ UI hiện → Bạn chạy "curl localhost:3000/api" → Nhập feedback → Submit
AI: "Tôi sẽ implement thêm error handling như bạn suggest."
```

## ⚙️ Settings Management

### **Project-specific Settings:**
- Mỗi project có cấu hình riêng
- Lưu trong `~/.config/InteractiveFeedbackMCP/` (Linux/macOS)
- Hoặc `%APPDATA%/InteractiveFeedbackMCP/` (Windows)

### **Các settings được lưu:**
- `run_command`: Command mặc định
- `execute_automatically`: Tự động chạy
- `commandSectionVisible`: Hiển thị command section
- `geometry`: Vị trí và kích thước cửa sổ
- `windowState`: Trạng thái cửa sổ (normal/zoomed)

### **Real-time Updates:**
- Settings được lưu ngay khi thay đổi
- Không cần click Save (trừ khi muốn)
- Tự động khôi phục khi mở lại

## 💡 Tips sử dụng hiệu quả

### 1. **Sử dụng Command Section**
- **Test ngay**: Chạy tests, lints, builds
- **Verify changes**: Check git diff, logs
- **Debug**: Chạy debug commands

### 2. **Feedback có ý nghĩa**
- **Cụ thể**: "Function này cần error handling"
- **Constructive**: "Tốt, nhưng nên thêm validation"
- **Actionable**: "Cần refactor để dễ test hơn"

### 3. **Lưu cấu hình**
- **Auto-execute**: Tự động chạy commands quen thuộc
- **Save config**: Lưu commands cho từng project

### 4. **Workflow tối ưu**
1. AI implement → UI hiện
2. Chạy tests/commands → Xem output
3. Nhập feedback cụ thể → Submit
4. AI cải thiện → Lặp lại

## 🔧 Troubleshooting

### **UI không hiển thị:**
```bash
# Test tkinter
uv run python -c "import tkinter; print('OK')"

# Test UI trực tiếp
uv run python test_ui_direct.py
```

### **Server không chạy:**
```bash
# Test server
uv run python server_tkinter.py

# Check logs
uv run fastmcp dev server_tkinter.py
```

### **Settings không lưu:**
- Kiểm tra quyền ghi file
- Kiểm tra đường dẫn settings directory
- Xem logs trong console

### **Commands không chạy:**
- Kiểm tra working directory
- Kiểm tra permissions
- Sử dụng full path nếu cần

## 📁 File Structure

```
interactive-feedback-mcp/
├── server_tkinter.py          # MCP Server (Tkinter)
├── feedback_ui_tkinter.py     # UI (Tkinter)
├── settings_manager.py        # Settings Manager
├── mcp.json                   # Cursor config
├── test_ui_direct.py          # Test UI
├── CURSOR_SETUP.md            # Setup guide
├── FEATURE_COMPARISON_UPDATED.md # Feature comparison
└── COMPLETE_GUIDE.md          # Complete guide (this file)
```

## 🆚 So sánh với bản gốc

| Tính năng | PySide6 | Tkinter | Ghi chú |
|-----------|---------|---------|---------|
| **UI Components** | ✅ | ✅ | 100% tương đương |
| **Core Functionality** | ✅ | ✅ | 100% tương đương |
| **Settings Persistence** | ✅ | ✅ | 100% tương đương |
| **Advanced Features** | ✅ | ✅ | 100% tương đương |
| **Cross-platform** | ⚠️ | ✅ | Tkinter tốt hơn |
| **Dependencies** | ❌ | ✅ | Tkinter nhẹ hơn |
| **Performance** | ✅ | ✅ | Tương đương |

## 🎉 Kết quả

Với Interactive Feedback MCP, bạn sẽ:
- **Tiết kiệm thời gian**: Ít back-and-forth với AI
- **Giảm chi phí**: Ít premium requests
- **Cải thiện chất lượng**: Feedback trực tiếp, cụ thể
- **Tăng hiệu suất**: Workflow mượt mà hơn

## 🎯 Kết luận

**Interactive Feedback MCP (Tkinter Version) đã hoàn thiện 100%!**

- ✅ **Đầy đủ tính năng** như bản gốc PySide6
- ✅ **Cross-platform** hoạt động mọi OS
- ✅ **Không dependencies** phụ thuộc
- ✅ **Performance cao** và ổn định
- ✅ **Sẵn sàng sử dụng** trong Cursor

**Bắt đầu sử dụng ngay để tăng hiệu suất AI development!** 🚀

## 📞 Hỗ trợ

- **GitHub**: https://github.com/noopstudios/interactive-feedback-mcp
- **Author**: Fábio Ferreira (@fabiomlferreira)
- **Website**: https://dotcursorrules.com
