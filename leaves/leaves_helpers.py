import os
import re
import pandas as pd
from datetime import datetime

# =========================================================
# PATHS
# =========================================================

ATTACHMENTS_DIR = "data/leave_attachments"

os.makedirs(
    ATTACHMENTS_DIR,
    exist_ok=True
)

# =========================================================
# SAFE STRING
# =========================================================

def safe_str(v):

    if pd.isna(v):
        return ""

    return str(v).strip()


# =========================================================
# FORMAT DATE
# =========================================================

def fmt_date(v):

    try:

        if pd.isna(v):
            return ""

        return pd.to_datetime(v).strftime("%Y-%m-%d")

    except Exception:

        return ""


# =========================================================
# NORMALIZE EMPLOYEE ID
# =========================================================

def normalize_emp_id(v):

    return (
        safe_str(v)
        .replace(".0", "")
        .strip()
    )


# =========================================================
# SANITIZE FILE NAME
# =========================================================

def sanitize_filename(name):

    if not name:
        return ""

    name = re.sub(
        r'[\\/*?:"<>|]',
        "_",
        str(name)
    )

    return name.strip()


# =========================================================
# EMPLOYEE LABEL
# =========================================================

def employee_option_label(row):

    emp_no = normalize_emp_id(
        row.get("employee_no")
    )

    name_ar = safe_str(
        row.get("name_ar")
    )

    dept = safe_str(
        row.get("department")
    )

    return f"{name_ar} | {emp_no} | {dept}"


# =========================================================
# FIND EMPLOYEE
# =========================================================

def find_employee_record(df, key):

    if df is None or df.empty:
        return None

    key = normalize_emp_id(key)

    for _, row in df.iterrows():

        emp_id = normalize_emp_id(
            row.get("employee_id")
        )

        emp_no = normalize_emp_id(
            row.get("employee_no")
        )

        if key in [emp_id, emp_no]:

            return row.to_dict()

    return None


# =========================================================
# SAVE ATTACHMENT
# =========================================================

def save_leave_attachment(

    uploaded_file,
    employee_id,
    start_date,
    end_date

):

    if uploaded_file is None:

        return "", ""

    try:

        employee_id = normalize_emp_id(
            employee_id
        )

        ext = os.path.splitext(
            uploaded_file.name
        )[1]

        filename = (

            f"{employee_id}_"

            f"{pd.Timestamp(start_date).strftime('%Y%m%d')}_"

            f"{pd.Timestamp(end_date).strftime('%Y%m%d')}_"

            f"{datetime.now().strftime('%H%M%S')}"

            f"{ext}"

        )

        filename = sanitize_filename(
            filename
        )

        file_path = os.path.join(
            ATTACHMENTS_DIR,
            filename
        )

        with open(file_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )

        return filename, file_path

    except Exception:

        return "", ""