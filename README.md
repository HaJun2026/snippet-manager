# snippet-manager

Code snippet manager CLI — lưu và tra cứu các đoạn code hữu ích trong quá trình học lập trình.

## Cài đặt

Không cần `pip install`. Chỉ cần Python 3.8+.

```bash
python snippet.py --help
```

## Lệnh

| Lệnh | Mô tả |
|------|-------|
| `add "title" "code" --lang py --tags tag1 tag2 --note "..."` | Lưu snippet mới |
| `list [--lang python] [--tag pattern]` | Liệt kê snippets |
| `show <id>` | Hiển thị snippet đầy đủ |
| `search <keyword>` | Tìm theo từ khoá |
| `delete <id>` | Xoá snippet |
| `export [--output file.md] [--lang python]` | Xuất ra Markdown |
| `stats` | Thống kê sử dụng |

## Ví dụ

```bash
# Lưu một snippet
python snippet.py add "List comprehension với điều kiện" \
  "[x*2 for x in range(10) if x % 2 == 0]" \
  --lang python --tags python pattern --note "Lọc và transform trong 1 dòng"

# Tìm kiếm
python snippet.py search "decorator"

# Xem snippet #3
python snippet.py show 3

# Xuất tất cả snippet Python
python snippet.py export --lang python --output python_snippets.md
```

## Lưu trữ

Snippets được lưu tại `~/.snippets.json` — không bị mất khi update code.

## Templates

Xem thư mục `templates/` để có sẵn các pattern phổ biến:
- `python_patterns.md`
- `web_patterns.md`

## Tích hợp với Claude Code

Dùng skill `/snippet` trong Claude Code để lưu snippets tự động từ hội thoại.
