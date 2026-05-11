import pandas as pd

from database.leaves_db import load_leaves_db


WEEKDAY_AR = {
    "Saturday": "السبت",
    "Sunday": "الأحد",
    "Monday": "الإثنين",
    "Tuesday": "الثلاثاء",
    "Wednesday": "الأربعاء",
    "Thursday": "الخميس",
    "Friday": "الجمعة",
}


# =========================================================
# NORMALIZE ID
# =========================================================

def normalize_id(v):

    try:

        v = str(v).strip()

        if v.endswith(".0"):

            v = v[:-2]

        return v

    except Exception:

        return ""


# =========================================================
# MINUTES TO HHMM
# =========================================================

def minutes_to_hhmm(minutes):

    try:

        minutes = int(minutes or 0)

    except Exception:

        minutes = 0

    sign = "-" if minutes < 0 else ""

    minutes = abs(minutes)

    return f"{sign}{minutes // 60:02}:{minutes % 60:02}"


# =========================================================
# FIND COLUMN
# =========================================================

def find_column(df, possible_names):

    for col in df.columns:

        clean_col = str(col).strip().lower()

        for name in possible_names:

            if clean_col == name.lower():

                return col

    return None


# =========================================================
# PARSE TIME
# =========================================================

def parse_time_col(series):

    return pd.to_datetime(
        series.astype(str).str.strip(),
        format="%H:%M:%S",
        errors="coerce"
    )


# =========================================================
# LOAD LEAVES
# =========================================================

def prepare_leaves():

    leaves = load_leaves_db()

    if leaves is None or leaves.empty:

        return pd.DataFrame()

    leaves = leaves.copy()

    if "employee_id" not in leaves.columns:

        leaves["employee_id"] = ""

    if "leave_type" not in leaves.columns:

        leaves["leave_type"] = ""

    if "status" not in leaves.columns:

        leaves["status"] = ""

    leaves["employee_id"] = (
        leaves["employee_id"]
        .apply(normalize_id)
    )

    leaves["start_date"] = pd.to_datetime(
        leaves["start_date"],
        errors="coerce"
    ).dt.floor("D")

    leaves["end_date"] = pd.to_datetime(
        leaves["end_date"],
        errors="coerce"
    ).dt.floor("D")

    return leaves


# =========================================================
# FIND LEAVE
# =========================================================

def find_leave_for_day(
    leaves_df,
    employee_id,
    day
):

    if leaves_df.empty:

        return False, ""

    emp_id = normalize_id(employee_id)

    check_date = pd.to_datetime(day).normalize()

    emp_leaves = leaves_df[
        leaves_df["employee_id"] == emp_id
    ]

    if emp_leaves.empty:

        return False, ""

    hit = emp_leaves[
        (emp_leaves["start_date"] <= check_date)
        &
        (emp_leaves["end_date"] >= check_date)
    ]

    if hit.empty:

        return False, ""

    leave_type = str(
        hit.iloc[0].get(
            "leave_type",
            "إجازة"
        )
    )

    return True, leave_type


# =========================================================
# MAIN
# =========================================================

def process_attendance(

    uploaded_file,

    work_start="08:00",

    grace_minutes=15,

    employees_df=None
):

    if uploaded_file is None:

        return pd.DataFrame()

    # =====================================================
    # RAW
    # =====================================================

    raw = pd.read_excel(
        uploaded_file,
        header=None
    )

    header_row = None

    for i in range(min(10, len(raw))):

        vals = [

            str(x).strip().lower()

            for x in raw.iloc[i].tolist()
        ]

        if (
            "employee id" in vals
            and
            "date" in vals
        ):

            header_row = i

            break

    if header_row is None:

        raise Exception(
            "لم يتم العثور على صف العناوين"
        )

    # =====================================================
    # READ FILE
    # =====================================================

    df = pd.read_excel(
        uploaded_file,
        header=header_row
    )

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # =====================================================
    # FIND COLUMNS
    # =====================================================

    employee_id_col = find_column(
        df,
        ["Employee ID"]
    )

    employee_name_col = find_column(
        df,
        ["First Name"]
    )

    department_col = find_column(
        df,
        ["Department"]
    )

    date_col = find_column(
        df,
        ["Date"]
    )

    first_punch_col = find_column(
        df,
        ["First Punch"]
    )

    last_punch_col = find_column(
        df,
        ["Last Punch"]
    )

    rename_map = {

        employee_id_col: "employee_id",

        employee_name_col: "employee_name",

        department_col: "department",

        date_col: "date",

        first_punch_col: "first_punch",

        last_punch_col: "last_punch",
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    # =====================================================
    # CLEAN
    # =====================================================

    df["employee_id"] = (
        df["employee_id"]
        .apply(normalize_id)
    )
    
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )
    
    # حذف الصفوف التي لا تحتوي تاريخ صحيح
    df = df[
        df["date"].notna()
    ].copy()
    
    df["date"] = df["date"].dt.floor("D")

    df["first_punch"] = parse_time_col(
        df["first_punch"]
    )

    df["last_punch"] = parse_time_col(
        df["last_punch"]
    )

    # =====================================================
    # EMPLOYEES FILE
    # =====================================================

    if employees_df is not None and not employees_df.empty:

        emp = employees_df.copy()

        emp = emp.rename(columns={

            "Personnel Number": "employee_id",

            "Arabic name": "employee_name",

            "Nationality": "nationality",

            "الجنسية": "nationality",
        })

        if "nationality" not in emp.columns:

            emp["nationality"] = ""

        emp["employee_id"] = (
            emp["employee_id"]
            .apply(normalize_id)
        )

        emp = emp[
            [
                "employee_id",
                "employee_name",
                "nationality"
            ]
        ].drop_duplicates()

        df = df.merge(

            emp,

            on="employee_id",

            how="left",

            suffixes=("", "_emp")
        )

        if "employee_name_emp" in df.columns:

            df["employee_name"] = (
                df["employee_name_emp"]
                .fillna(df["employee_name"])
            )

        if "nationality" not in df.columns:

            df["nationality"] = ""

    else:

        df["nationality"] = ""

    # =====================================================
    # WEEKDAY
    # =====================================================

    df["weekday"] = (
        df["date"].dt.day_name()
    )

    df["weekday_ar"] = (
        df["weekday"].map(WEEKDAY_AR)
    )

    # =====================================================
    # SETTINGS
    # =====================================================

    start_hour = int(
        work_start.split(":")[0]
    )

    start_minute = int(
        work_start.split(":")[1]
    )

    start_minutes = (
        start_hour * 60
        +
        start_minute
    )

    late_limit_minutes = (
        start_minutes
        +
        int(grace_minutes)
    )

    end_minutes = 17 * 60

    # =====================================================
    # LATE
    # =====================================================

    def calc_late(row):

        if row["weekday"] == "Saturday":

            return 0

        if pd.isna(row["first_punch"]):

            return 0

        actual = (
            row["first_punch"].hour * 60
            +
            row["first_punch"].minute
        )

        return max(
            0,
            actual - late_limit_minutes
        )

    # =====================================================
    # EARLY LEAVE
    # =====================================================

    def calc_early(row):

        if row["weekday"] == "Saturday":

            return 0

        if pd.isna(row["last_punch"]):

            return 0

        actual = (
            row["last_punch"].hour * 60
            +
            row["last_punch"].minute
        )

        return max(
            0,
            end_minutes - actual
        )

    # =====================================================
    # OVERTIME
    # =====================================================

    def calc_ot(row):

        if row["weekday"] == "Saturday":

            return 0

        if pd.isna(row["last_punch"]):

            return 0

        actual = (
            row["last_punch"].hour * 60
            +
            row["last_punch"].minute
        )

        return max(
            0,
            actual - end_minutes
        )

    # =====================================================
    # WORK HOURS
    # =====================================================

    def calc_work(row):

        nationality = str(
            row.get("nationality", "")
        ).strip().lower()

        # السعودي السبت إجازة
        if (
            row["weekday"] == "Saturday"
            and
            nationality in [
                "saudi",
                "saudi arabia",
                "سعودي",
                "السعودية"
            ]
        ):

            return 0

        if pd.isna(row["first_punch"]):

            return 0

        if pd.isna(row["last_punch"]):

            return 0

        diff = (
            row["last_punch"]
            -
            row["first_punch"]
        )

        return max(
            0,
            int(diff.total_seconds() // 60)
        )

    # =====================================================
    # CALCULATIONS
    # =====================================================

    df["late_minutes"] = df.apply(
        calc_late,
        axis=1
    )

    df["early_leave_minutes"] = df.apply(
        calc_early,
        axis=1
    )

    df["overtime_minutes"] = df.apply(
        calc_ot,
        axis=1
    )

    df["worked_minutes"] = df.apply(
        calc_work,
        axis=1
    )

    # =====================================================
    # FORMAT
    # =====================================================

    df["late_hhmm"] = (
        df["late_minutes"]
        .apply(minutes_to_hhmm)
    )

    df["early_leave_hhmm"] = (
        df["early_leave_minutes"]
        .apply(minutes_to_hhmm)
    )

    df["overtime_hhmm"] = (
        df["overtime_minutes"]
        .apply(minutes_to_hhmm)
    )

    df["work_hours"] = (
        df["worked_minutes"]
        .apply(minutes_to_hhmm)
    )

    # =====================================================
    # LEAVES
    # =====================================================

    leaves_df = prepare_leaves()

    statuses = []

    leave_types = []

    for _, row in df.iterrows():

        is_leave, leave_type = (
            find_leave_for_day(
                leaves_df,
                row["employee_id"],
                row["date"]
            )
        )

        if is_leave:

            statuses.append(
                f"إجازة - {leave_type}"
            )

            leave_types.append(
                leave_type
            )

        else:

            if row["weekday"] == "Saturday":

                if pd.isna(
                    row["first_punch"]
                ):

                    statuses.append("غائب")

                else:

                    statuses.append("حاضر")

            else:

                if row["late_minutes"] > 0:

                    statuses.append("متأخر")

                else:

                    statuses.append("حاضر")

            leave_types.append("")

    df["status"] = statuses

    df["leave_type"] = leave_types

    return df
