# Worksheet: Phân tích & Đánh giá Data Model (Lab 5)

## Nhiệm vụ H3 (Bonus): Phân tích thiết kế bảng trong `bad_schema.sql`

Bảng `chats` trong file `bad_schema.sql` gặp nhiều lỗi thiết kế cơ bản về chuẩn hóa dữ liệu, hiệu năng và tính toàn vẹn. Dưới đây là 3 vấn đề tiêu biểu và giải pháp khắc phục dựa trên thiết kế của bài lab.

---

### Vấn đề 1: Dư thừa dữ liệu và Vi phạm Chuẩn hóa (Redundancy & Update Anomaly)

* **Hiện trạng:**
  Hai cột `student_name` và `student_phone` được lưu trực tiếp trên từng bản ghi tin nhắn. 

* **Hậu quả:**
  Lãng phí dung lượng và gây nguy cơ bất nhất dữ liệu (Update Anomaly). Nếu sinh viên đổi số điện thoại, hệ thống phải cập nhật trên tất cả các dòng tin nhắn cũ; nếu sót sẽ dẫn đến dữ liệu sai lệch.

* **Cách khắc phục:**
  Tách thực thể sinh viên ra một bảng độc lập. Trong bảng `chats` chỉ lưu khóa ngoại `student_id`.

**Minh họa thiết kế mới:**
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT
);

CREATE TABLE chats (
    id INTEGER PRIMARY KEY,
    student_id INTEGER, -- Khóa ngoại tham chiếu bảng students
    message TEXT,
    ...
);
```

---

### Vấn đề 2: Vi phạm Dạng chuẩn 1 (1NF) - Dữ liệu không nguyên tử

* **Hiện trạng:**
  Cột `feedback TEXT` lưu danh sách các giá trị đánh giá được phân cách bằng dấu phẩy (ví dụ: `'1,-1,1'`).

* **Hậu quả:**
  Vi phạm Dạng chuẩn 1 (1NF) vì một ô chứa nhiều giá trị. Không thể sử dụng trực tiếp các hàm tổng hợp như `AVG()`, `COUNT()` trong SQL để tính điểm, và tìm kiếm sẽ rất chậm.

* **Cách khắc phục:**
  Tách dữ liệu đánh giá ra một bảng riêng biệt. Mỗi lượt phản hồi là một dòng liên kết với `chat_id`.

**Minh họa thiết kế mới:**
```sql
CREATE TABLE feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER, -- Khóa ngoại tham chiếu bảng chats
    rating INTEGER,  -- 1, 0, hoặc -1
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Vấn đề 3: Sai kiểu dữ liệu, Thiếu ràng buộc và Lưu trữ đơn vị trong giá trị

* **Hiện trạng:**
  - Thiếu `PRIMARY KEY` cho cột `id`.
  - Cột `time TEXT` lưu chuỗi ngày giờ định dạng tự do (`'5/10/2026 9:03 PM'`).
  - Cột `latency TEXT` lưu cả giá trị và đơn vị đo lường (`'120ms'`).

* **Hậu quả:**
  - Mất tính duy nhất của bản ghi.
  - Chuỗi thời gian không theo chuẩn ISO khiến việc sắp xếp (`ORDER BY`) hay lọc (`BETWEEN`) bị sai.
  - Cột `latency` chứa chữ "ms" làm mất khả năng thực hiện phép toán thống kê (min, max, avg).

* **Cách khắc phục:**
  - Thêm `PRIMARY KEY`.
  - Sử dụng `TIMESTAMP` hoặc `DATETIME` theo chuẩn ISO 8601.
  - Đổi kiểu `latency` thành `INTEGER` để lưu giá trị số (miligiây).

**Minh họa thiết kế mới:**
```sql
CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latency_ms INTEGER -- Lưu dạng số nguyên, vd: 120
);
```