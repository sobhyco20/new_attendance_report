import sqlite3
import pandas as pd

# =========================================================
# DATABASE
# =========================================================

DB_PATH = "attendance.db"

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================================
# CREATE TABLE
# =========================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS leaves (

    leave_id TEXT PRIMARY KEY,

    employee_id TEXT,
    employee_no TEXT,

    name_ar TEXT,
    name_en TEXT,

    department TEXT,
    job_title TEXT,

    leave_type TEXT,

    start_date TEXT,
    end_date TEXT,

    status TEXT,

    attachment_name TEXT,
    attachment_path TEXT,

    notes TEXT,

    created_at TEXT,
    created_by TEXT
)

""")

conn.commit()

# =========================================================
# LOAD ALL LEAVES
# =========================================================

def load_leaves_db():

    try:

        df = pd.read_sql(

            """
            SELECT *
            FROM leaves
            ORDER BY start_date DESC
            """,

            conn
        )

        return df

    except Exception:

        return pd.DataFrame()


# =========================================================
# EXPORT TO EXCEL
# =========================================================

def export_leaves_excel():

    try:

        df = load_leaves_db()

        df.to_excel(

            "data/leaves.xlsx",

            index=False
        )

    except Exception:

        pass

# =========================================================
# INSERT LEAVE
# =========================================================

def insert_leave(record: dict):

    cursor.execute("""

    INSERT OR REPLACE INTO leaves (

        leave_id,

        employee_id,
        employee_no,

        name_ar,
        name_en,

        department,
        job_title,

        leave_type,

        start_date,
        end_date,

        status,

        attachment_name,
        attachment_path,

        notes,

        created_at,
        created_by

    )

    VALUES (

        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

    )

    """, (

        record.get("leave_id"),

        record.get("employee_id"),
        record.get("employee_no"),

        record.get("name_ar"),
        record.get("name_en"),

        record.get("department"),
        record.get("job_title"),

        record.get("leave_type"),

        str(record.get("start_date")),
        str(record.get("end_date")),

        record.get("status"),

        record.get("attachment_name"),
        record.get("attachment_path"),

        record.get("notes"),

        str(record.get("created_at")),
        record.get("created_by"),
    ))

    conn.commit()
    export_leaves_excel()
# =========================================================
# UPDATE LEAVE
# =========================================================

def update_leave_db(record: dict):

    cursor.execute("""

    UPDATE leaves

    SET

        leave_type=?,

        start_date=?,
        end_date=?,

        status=?,

        attachment_name=?,
        attachment_path=?,

        notes=?

    WHERE leave_id=?

    """, (

        record.get("leave_type"),

        str(record.get("start_date")),
        str(record.get("end_date")),

        record.get("status"),

        record.get("attachment_name"),
        record.get("attachment_path"),

        record.get("notes"),

        record.get("leave_id"),
    ))

    conn.commit()
    export_leaves_excel()
# =========================================================
# DELETE LEAVE
# =========================================================

def delete_leave(leave_id):

    cursor.execute(

        """
        DELETE FROM leaves
        WHERE leave_id=?
        """,

        (str(leave_id),)
    )

    conn.commit()
    export_leaves_excel()
# =========================================================
# GET EMPLOYEE LEAVES
# =========================================================

def get_employee_leaves(employee_id):

    try:

        query = """

        SELECT *
        FROM leaves

        WHERE employee_id=?

        ORDER BY start_date DESC

        """

        df = pd.read_sql(
            query,
            conn,
            params=(str(employee_id),)
        )

        return df

    except Exception:

        return pd.DataFrame()

# =========================================================
# CHECK LEAVE
# =========================================================

def is_employee_on_leave(

    employee_id,

    check_date
):

    try:

        check_date = pd.to_datetime(
            check_date
        ).normalize()

        leaves = load_leaves_db()

        if leaves.empty:
            return False, ""

        leaves["start_date"] = pd.to_datetime(

            leaves["start_date"],

            errors="coerce"

        ).dt.normalize()

        leaves["end_date"] = pd.to_datetime(

            leaves["end_date"],

            errors="coerce"

        ).dt.normalize()

        # =========================================
        # NORMALIZE IDS
        # =========================================

        def normalize_id(v):

            try:

                v = str(v).strip()

                if v.endswith(".0"):
                    v = v[:-2]

                return v

            except Exception:

                return ""

        emp_id = normalize_id(employee_id)

        leaves["employee_id_clean"] = (

            leaves["employee_id"]

            .apply(normalize_id)
        )

        emp_leaves = leaves[

            leaves["employee_id_clean"]

            ==

            emp_id
        ]

        for _, row in emp_leaves.iterrows():

            start = row["start_date"]

            end = row["end_date"]

            if pd.isna(start):
                continue

            if pd.isna(end):
                continue

            if start <= check_date <= end:

                return True, row.get(
                    "leave_type",
                    "إجازة"
                )

        return False, ""

    except Exception:

        return False, ""

# =========================================================
# IMPORT EXCEL LEAVES
# =========================================================

def import_leaves_excel(uploaded_file):

    try:

        df = pd.read_excel(
            uploaded_file
        )

        if df.empty:
            return 0

        df.columns = [

            str(c).strip()

            for c in df.columns
        ]

        required = [

            "employee_id",
            "leave_type",
            "start_date",
            "end_date"
        ]

        missing = []

        for c in required:

            if c not in df.columns:
                missing.append(c)

        if missing:

            raise Exception(
                f"الأعمدة غير موجودة: {missing}"
            )

        inserted = 0

        for _, row in df.iterrows():

            record = {

                "leave_id": str(
                    row.get(
                        "leave_id",
                        f"LV-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S%f')}"
                    )
                ),

                "employee_id": str(
                    row.get("employee_id", "")
                ),

                "employee_no": str(
                    row.get("employee_no", "")
                ),

                "name_ar": str(
                    row.get("name_ar", "")
                ),

                "name_en": str(
                    row.get("name_en", "")
                ),

                "department": str(
                    row.get("department", "")
                ),

                "job_title": str(
                    row.get("job_title", "")
                ),

                "leave_type": str(
                    row.get("leave_type", "إجازة")
                ),

                "start_date": str(
                    row.get("start_date")
                ),

                "end_date": str(
                    row.get("end_date")
                ),

                "status": str(
                    row.get("status", "معتمدة")
                ),

                "attachment_name": str(
                    row.get("attachment_name", "")
                ),

                "attachment_path": str(
                    row.get("attachment_path", "")
                ),

                "notes": str(
                    row.get("notes", "")
                ),

                "created_at": str(
                    pd.Timestamp.now()
                ),

                "created_by": "excel_import",
            }

            insert_leave(record)

            inserted += 1

        return inserted

    except Exception as e:

        raise Exception(
            f"فشل استيراد الإجازات: {e}"
        )