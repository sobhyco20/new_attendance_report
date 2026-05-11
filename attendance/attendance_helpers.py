import pandas as pd

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

        return pd.to_datetime(v).strftime(
            "%Y-%m-%d"
        )

    except Exception:

        return ""


# =========================================================
# FORMAT TIME
# =========================================================

def fmt_time(v):

    try:

        if pd.isna(v):
            return ""

        return pd.to_datetime(v).strftime(
            "%H:%M"
        )

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
# MINUTES TO HH:MM
# =========================================================

def minutes_to_hhmm(minutes):

    try:

        minutes = int(minutes)

        h = minutes // 60

        m = minutes % 60

        return f"{h:02}:{m:02}"

    except Exception:

        return "00:00"