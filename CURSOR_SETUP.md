# Hướng dẫn cấu hình Interactive Feedback MCP trong Cursor

## Vấn đề đã được giải quyết

Vấn đề ban đầu là PySide6 không thể cài đặt được trên macOS. Tôi đã tạo một phiên bản thay thế sử dụng tkinter (có sẵn trong Python) thay vì PySide6.

## Files đã tạo

1. `server_tkinter.py` - Server MCP sử dụng tkinter
2. `feedback_ui_tkinter.py` - UI sử dụng tkinter thay vì PySide6

## Cấu hình trong Cursor

### Bước 1: Tạo file cấu hình MCP

Tạo file `mcp.json` trong thư mục cấu hình của Cursor (thường là `~/.cursor/mcp.json` hoặc trong settings của Cursor):

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
      "autoApprove": [
        "interactive_feedback"
      ]
    }
  }
}
```

### Bước 2: Thêm prompt rule vào Cursor

Thêm rule sau vào custom prompt của Cursor:

```
Whenever you want to ask a question, always call the MCP `interactive_feedback`.
Whenever you're about to complete a user request, call the MCP `interactive_feedback` instead of simply ending the process. Keep calling MCP until the user's feedback is empty, then end the request.
```

### Bước 3: Test cấu hình

1. Khởi động lại Cursor
2. Mở một project bất kỳ
3. Yêu cầu AI thực hiện một task
4. AI sẽ gọi MCP `interactive_feedback` và hiển thị UI

## Cách sử dụng

1. Khi AI gọi `interactive_feedback`, một cửa sổ UI sẽ xuất hiện
2. Bạn có thể:
   - Xem feedback từ AI
   - Chạy commands trong project directory
   - Nhập feedback cho AI
   - Lưu cấu hình cho project

## Troubleshooting

### Nếu UI không hiển thị:
- Kiểm tra xem tkinter có hoạt động: `uv run python -c "import tkinter; print('OK')"`
- Kiểm tra logs của Cursor để xem có lỗi gì không

### Nếu server không chạy:
- Kiểm tra đường dẫn trong `mcp.json` có đúng không
- Chạy thử: `cd /Users/btk0092/Documents/mcp/interactive-feedback-mcp && uv run server_tkinter.py`

## Khác biệt với phiên bản gốc

- Sử dụng tkinter thay vì PySide6 (không cần cài đặt thêm dependencies)
- UI đơn giản hơn nhưng vẫn đầy đủ chức năng
- Tương thích tốt hơn với macOS

## Lưu ý

- Đảm bảo Python 3.11+ đã được cài đặt
- Đảm bảo `uv` đã được cài đặt
- Có thể cần cấp quyền cho Cursor truy cập terminal
