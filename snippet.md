# /snippet — Lưu và tra cứu code snippets

Skill này tích hợp với CLI tool `snippet.py` để lưu các đoạn code hữu ích trong quá trình học.

**Repo GitHub:** `https://github.com/HaJun2026/snippet-manager`
**Local tool:** `.claude/commands/snippet/snippet.py`
**Templates:** `.claude/commands/snippet/templates/`

---

## Cách dùng

### Lưu snippet từ code đang xem
```
/snippet lưu
```
Đọc code người dùng paste vào, đặt title ngắn gọn, tự động detect ngôn ngữ và đề xuất tags.
Sau đó chạy:
```bash
python .claude/commands/snippet/snippet.py add "title" "code" --lang python --tags pattern decorator --note "giải thích ngắn"
```

### Tìm snippet
```
/snippet tìm [từ khoá]
```
```bash
python .claude/commands/snippet/snippet.py search "từ khoá"
```

### Xem snippet theo ID
```
/snippet xem [id]
```
```bash
python .claude/commands/snippet/snippet.py show [id]
```

### Liệt kê theo ngôn ngữ hoặc tag
```
/snippet danh sách [python|js|...]
```
```bash
python .claude/commands/snippet/snippet.py list --lang python
python .claude/commands/snippet/snippet.py list --tag pattern
```

### Xuất ra Markdown (để push lên GitHub)
```
/snippet xuất
```
```bash
python .claude/commands/snippet/snippet.py export --output my_snippets.md
```

### Xoá snippet
```
/snippet xoá [id]
```
```bash
python .claude/commands/snippet/snippet.py delete [id]
```

### Thống kê
```
/snippet stats
```
```bash
python .claude/commands/snippet/snippet.py stats
```

---

## Templates sẵn có

Trong thư mục `templates/`:
- `python_patterns.md` — Context manager, dataclass, decorator, retry
- `web_patterns.md` — FastAPI endpoint, React hook, CSS utilities

Khi người dùng hỏi về pattern phổ biến, gợi ý xem templates trước khi tạo mới.

---

## Ngôn ngữ hỗ trợ (--lang)
`python` · `javascript` · `typescript` · `sql` · `bash` · `css` · `html` · `go` · `rust`

## Tags gợi ý
- `pattern` — design pattern, coding pattern
- `api` — gọi API, xử lý response
- `db` — database, query
- `auth` — authentication, authorization
- `util` — tiện ích tổng quát
- `async` — async/await, concurrency

---

## Luồng mặc định

Nếu không có tham số, hỏi người dùng:
> "Bạn muốn: (1) lưu snippet mới, (2) tìm kiếm, hay (3) xem danh sách?"

Khi lưu snippet, tự động:
1. Detect ngôn ngữ từ syntax
2. Đề xuất title mô tả rõ (không phải `snippet1`)
3. Gợi ý tags phù hợp
4. Hỏi có muốn thêm note giải thích không

---

## Kết nối với GitHub

Snippets quan trọng nên push lên `https://github.com/HaJun2026/snippet-manager`:
```bash
# Export rồi commit
python .claude/commands/snippet/snippet.py export --output snippets_export.md
# Sau đó git add, commit, push trong repo snippet-manager
```
