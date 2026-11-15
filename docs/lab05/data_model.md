# Worksheet: Data Model Analysis & Evaluation (Lab 5)

## Task H3 (Bonus): Analyze the table design in `bad_schema.sql`

The `chats` table in the `bad_schema.sql` file (as referenced in the "data_model.md" document) encounters multiple basic design flaws regarding data normalization, performance, and integrity. Below are 3 typical issues and their solutions based on the lab's design.

---

### Issue 1: Data Redundancy and Normalization Violation (Update Anomaly)

*   **Current State:** The two columns `student_name` and `student_phone` are stored directly on each message record.
*   **Consequences:** This wastes storage space and causes a risk of data inconsistency (Update Anomaly). If a student changes their phone number, the system must update it across all old message rows; missing any will result in inaccurate data.
*   **Solution:** Separate the student entity into an independent table. In the `chats` table, only store the `student_id` foreign key.

**New design illustration:**
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT
);

CREATE TABLE chats (
    id INTEGER PRIMARY KEY,
    student_id INTEGER, -- Foreign key referencing the students table
    message TEXT,
    ...
);
```

---

### Issue 2: First Normal Form (1NF) Violation - Non-atomic data

*   **Current State:** The `feedback TEXT` column stores a comma-separated list of rating values (e.g., `'1,-1,1'`).
*   **Consequences:** This violates the First Normal Form (1NF) because a single cell contains multiple values. Aggregate functions like `AVG()` and `COUNT()` in SQL cannot be directly used to calculate scores, and searching will be very slow.
*   **Solution:** Separate the feedback data into a distinct table. Each feedback entry is a row linked to the `chat_id`.

**New design illustration:**
```sql
CREATE TABLE feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER, -- Foreign key referencing the chats table
    rating INTEGER,  -- 1, 0, or -1
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Issue 3: Incorrect Data Types, Missing Constraints, and Storing Units in Values

*   **Current State:**
    *   Missing `PRIMARY KEY` for the `id` column.
    *   The `time TEXT` column stores free-format date and time strings (`'5/10/2026 9:03 PM'`).
    *   The `latency TEXT` column stores both the value and the unit of measurement (`'120ms'`).
*   **Consequences:**
    *   Loss of record uniqueness.
    *   Non-ISO standard time strings cause incorrect sorting (`ORDER BY`) or filtering (`BETWEEN`).
    *   The `latency` column containing the letters "ms" eliminates the ability to perform statistical operations (min, max, avg).
*   **Solution:**
    *   Add a `PRIMARY KEY`.
    *   Use `TIMESTAMP` or `DATETIME` following the ISO 8601 standard.
    *   Change the `latency` data type to `INTEGER` to store numerical values (milliseconds).

**New design illustration:**
```sql
CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latency_ms INTEGER -- Stored as an integer, e.g., 120
);
```