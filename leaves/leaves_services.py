import pandas as pd

from database.leaves_db import (
    load_leaves_db,
    insert_leave,
    update_leave_db,
    delete_leave
)

from leaves.leaves_helpers import (
    normalize_emp_id
)

# =========================================================
# LOAD LEAVES
# =========================================================

def load_leaves():

    df = load_leaves_db()

    if df is None or df.empty:

        return pd.DataFrame(columns=[

            "leave_id",

            "employee_id",
            "employee_no",

            "name_ar",
            "name_en",

            "department",
            "job_title",

            "leave_type",

            "start_date",
            "end_date",

            "status",

            "attachment_name",
            "attachment_path",

            "notes",

            "created_at",
            "created_by",
        ])

    # =====================================================
    # STRING COLUMNS
    # =====================================================

    string_cols = [

        "leave_id",

        "employee_id",
        "employee_no",

        "name_ar",
        "name_en",

        "department",
        "job_title",

        "leave_type",

        "status",

        "attachment_name",
        "attachment_path",

        "notes",

        "created_by"
    ]

    for c in string_cols:

        if c not in df.columns:
            df[c] = ""

        df[c] = df[c].astype(str)

    # =====================================================
    # IDS
    # =====================================================

    df["employee_id"] = df[
        "employee_id"
    ].apply(normalize_emp_id)

    df["employee_no"] = df[
        "employee_no"
    ].apply(normalize_emp_id)

    # =====================================================
    # DATES
    # =====================================================

    date_cols = [

        "start_date",
        "end_date",
        "created_at"
    ]

    for c in date_cols:

        if c in df.columns:

            df[c] = pd.to_datetime(
                df[c],
                errors="coerce"
            )

    return df


# =========================================================
# ADD
# =========================================================

def add_leave_record(record):

    insert_leave(record)


# =========================================================
# UPDATE
# =========================================================

def edit_leave_record(record):

    update_leave_db(record)


# =========================================================
# DELETE
# =========================================================

def remove_leave_record(leave_id):

    delete_leave(leave_id)
