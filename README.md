# flashcard-cli

CLI tool học flashcard bằng Python thuần (không cần cài thêm thư viện).

Cards được lưu tại `~/.flashcards.json`.

## Cài đặt

```bash
# Clone về
git clone https://github.com/HaJun2026/flashcard-cli.git
cd flashcard-cli

# Python 3.8+ là đủ, không cần pip install gì thêm
python flashcard.py --help
```

## Lệnh

```bash
# Thêm card
python flashcard.py add "List comprehension là gì?" "Cú pháp tạo list ngắn gọn: [x for x in iterable if condition]" --tag python

# Xem danh sách
python flashcard.py list
python flashcard.py list --tag python

# Ôn tập (5 card, ưu tiên card chưa thuộc)
python flashcard.py quiz --tag python --count 5

# Thống kê
python flashcard.py stats

# Xoá card
python flashcard.py delete 3
```

## Tích hợp với Claude Code

Dùng skill `/flashcard` trong Claude Code để tạo card tự động từ ghi chú học tập.

## Tags gợi ý

| Tag | Nội dung |
|-----|----------|
| `python` | Lập trình Python |
| `web` | HTML/CSS/JS/React/Next.js |
| `backend` | API, database, server |
| `general` | Kiến thức tổng quát |
