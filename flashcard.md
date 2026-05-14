# /flashcard — Tạo và ôn flashcard học tập

Skill này tích hợp với CLI tool `flashcard.py` (cùng thư mục) để quản lý flashcard học tập.

**Repo GitHub:** `https://github.com/HaJun2026/flashcard-cli`
**Local tool:** `.claude/commands/flashcard/flashcard.py`

---

## Cách dùng

### Tạo flashcard từ ghi chú hoặc chủ đề
```
/flashcard tạo [chủ đề hoặc paste nội dung]
```
Nếu người dùng paste nội dung → trích xuất 3–7 cặp Q&A từ nội dung đó.
Nếu chỉ cho chủ đề → **gọi sub-agent `researcher`** để thu thập thông tin trước, rồi tạo flashcard từ kết quả:

> Khi cần research: "Use the researcher sub-agent to summarize [chủ đề], then I'll create flashcards from the summary."

Sau đó lưu từng card:
```bash
python .claude/commands/flashcard/flashcard.py add "câu hỏi" "câu trả lời" --tag [chủ đề]
```

### Tạo flashcard từ code review
```
/flashcard code-review [paste code]
```
**Gọi sub-agent `code-reviewer`** để review code, rồi tạo flashcard từ những điểm học được:
- Lỗi tìm thấy → Q: "Đoạn code này có vấn đề gì?" A: "[mô tả lỗi và cách fix]"
- Pattern tốt → Q: "Khi nào nên dùng [pattern]?" A: "[giải thích]"

### Ôn tập
```
/flashcard ôn [tag]
```
```bash
python .claude/commands/flashcard/flashcard.py quiz --tag [tag] --count 10
```
Sau mỗi session, gọi `stats` để xem tiến độ:
```bash
python .claude/commands/flashcard/flashcard.py stats
```

### Xem danh sách
```
/flashcard danh sách [tag]
```
```bash
python .claude/commands/flashcard/flashcard.py list --tag [tag]
```

### Xoá card
```
/flashcard xoá [id]
```
```bash
python .claude/commands/flashcard/flashcard.py delete [id]
```

### Thống kê tiến độ học
```
/flashcard stats
```
```bash
python .claude/commands/flashcard/flashcard.py stats
```

---

## Tags gợi ý
- `python` — lập trình Python
- `web` — HTML/CSS/JS/React/Next.js
- `backend` — API, database, server
- `code-review` — bài học từ review code
- `general` — kiến thức tổng quát

---

## Tích hợp với Sub-agents

| Tình huống | Sub-agent được gọi | Kết quả |
|------------|-------------------|---------|
| `/flashcard tạo [chủ đề web]` | `researcher` | Research chủ đề → tạo flashcard từ tóm tắt |
| `/flashcard code-review [code]` | `code-reviewer` | Review code → tạo flashcard từ bugs & patterns |
| `/flashcard ôn` + kết quả kém | `researcher` | Tra cứu thêm về chủ đề đang yếu |

---

## Luồng mặc định

Nếu không có tham số, hỏi người dùng:
> "Bạn muốn: (1) tạo flashcard từ chủ đề/nội dung, (2) tạo từ code review, (3) ôn tập, hay (4) xem thống kê?"

Khi tạo flashcard, ưu tiên format:
- **Q:** Ngắn gọn, hỏi đúng 1 khái niệm
- **A:** Trả lời súc tích, thêm ví dụ code nếu liên quan đến lập trình
