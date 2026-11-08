# Worksheet: Data Model Analysis & Evaluation (Lab 5)

## Task H3 (Bonus): Analyzing Table Design in `bad_schema.sql`

The `chats` table in the `bad_schema.sql` file suffers from several basic design flaws regarding data normalization, performance, and integrity. Below are 3 typical issues and their solutions based on the lab's design.

---

### Issue 1: Data Redundancy and Normalization Violation (Redundancy & Update Anomaly)

- **Current State:**
  The `student_name` and `student_phone` columns are stored directly on every message record.

- **Consequences:**
  Wastes storage space and creates a risk of data inconsistency (Update Anomaly). If a student changes their phone number, the system must update it across all previous message rows; if any are missed, it leads to data discrepancies.

- **Solution:**
  Separate the student entity into an independent table. In the `chats` table, only store the `student_id` foreign key.

**New Design Illustration:**
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

### Issue 2: First Normal Form (1NF) Violation - Non-atomic Data

- **Current State:**
  The `feedback TEXT` column stores a list of rating values separated by commas (e.g., `'1,-1,1'`).

- **Consequences:**
  Violates First Normal Form (1NF) because a single cell contains multiple values. SQL aggregate functions like `AVG()` and `COUNT()` cannot be used directly to calculate scores, and searching will be extremely slow.

- **Solution:**
  Separate the feedback data into a distinct table. Each feedback entry becomes a row linked to the `chat_id`.

**New Design Illustration:**
```sql
CREATE TABLE feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER, -- Foreign key referencing the chats table
    rating INTEGER,  -- 1, 0, or -1
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Issue 3: Incorrect Data Types, Missing Constraints, and Storing Units within Values

- **Current State:**
  - Missing `PRIMARY KEY` for the `id` column.
  - The `time TEXT` column stores free-format date/time strings (`'5/10/2026 9:03 PM'`).
  - The `latency TEXT` column stores both the value and the unit of measurement (`'120ms'`).

- **Consequences:**
  - Loss of record uniqueness.
  - Non-ISO standard time strings cause incorrect sorting (`ORDER BY`) or filtering (`BETWEEN`).
  - The `latency` column contains the text "ms", making statistical calculations (min, max, avg) impossible.

- **Solution:**
  - Add a `PRIMARY KEY`.
  - Use `TIMESTAMP` or `DATETIME` following the ISO 8601 standard.
  - Change the `latency` data type to `INTEGER` to store numerical values (milliseconds).

**New Design Illustration:**
```sql
CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latency_ms INTEGER -- Store as an integer, e.g., 120
);
```