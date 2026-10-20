# Lab 3 — AI extension review

1. Ask an AI coding assistant to extend your service with ONE feature, e.g. "Add an 'exam absence' answer that tells students the deadline from the handbook."

2. Paste the prompt you used:
> "Hãy bổ sung tính năng tính học phí (tuition) và xử lý phân tích số tín chỉ học lại (parse_credits) cho dự án assistant_core_lab, đồng thời viết unit test tương ứng."

3. Review the generated code manually. Document at least three changes you made:

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| 1 | Các đoạn mã trong `knowledge.py` và `tools.py` sử dụng các thư viện như `re`, `csv`, `dataclass` nhưng thiếu lệnh `import`. | Gây ra lỗi tô màu đỏ trong Editor và lỗi runtime `NameError` khi thực thi do biến/thư viện chưa được khai báo. | Thêm các dòng `import re`, `import csv`, `from dataclasses import dataclass`, `from pathlib import Path` ở đầu file. | Đảm bảo mã nguồn hợp lệ, trình quản lý mã nguồn nhận diện đúng các hàm và kiểu dữ liệu. |
| 2 | Các câu lệnh `import` bị thụt lùi đầu dòng (space dư thừa) hoặc có dòng trống ở trên cùng. | Bị lỗi cú pháp (IndentationError) hoặc vi phạm chuẩn định dạng mã nguồn PEP 8. | Định dạng lại mã nguồn: xóa khoảng trắng ở đầu các câu lệnh `import`, đưa sát về mép trái và căn chỉnh lại các hàm. | Giữ cho cấu trúc mã nguồn sạch sẽ, tuân thủ tiêu chuẩn PEP 8 của Python. |
| 3 | File test `tests/test_tools.py` gọi các hàm `parse_credits`, `tuition` và ngoại lệ `InvalidRequest` nhưng chưa import chúng. | Framework `pytest` không thể chạy được các bài unit test và báo lỗi thiếu biến/hàm. | Bổ sung `import pytest` và import các hàm `parse_credits`, `tuition`, `InvalidRequest` từ module gốc vào file test. | Giúp bộ kiểm thử tự động (unit tests) chạy thành công và xác minh đúng logic của tính năng mới. |

Checklist: interfaces respected? new dependencies? secrets? logging of user data? tests added and meaningful? Record the use in `docs/ai-use-log.md`.