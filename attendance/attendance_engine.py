import pandas as pd

from attendance.attendance_helpers import normalize_emp_id

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


def normalize_id(v):
    try:
        v = str(v).strip()
        if v.endswith(".0"):
            v = v[:-2]
        return v
    except Exception:
        return ""


def find_column(df, possible_names):
    for col in df.columns:
        clean_col = str(col).strip().lower()
        for name in possible_names:
            if clean_col == name.lower():
                return col
    return None


def minutes_to_hhmm(minutes):

    try:

        if pd.isna(minutes):

            minutes = 0

        minutes = int(float(minutes))

    except Exception:

        minutes = 0

    sign = "-" if minutes < 0 else ""

    minutes = abs(minutes)

    hours = int(minutes // 60)

    mins = int(minutes % 60)

    return f"{sign}{hours:02}:{mins:02}"


def parse_time_col(series):
    return pd.to_datetime(
        series.astype(str).str.strip(),
        format="%H:%M:%S",
        errors="coerce"
    )


def get_attendance_period(any_date):
    d = pd.to_datetime(any_date)

    if d.day >= 8:
        start_date = pd.Timestamp(year=d.year, month=d.month, day=8)

        if d.month == 12:
            end_date = pd.Timestamp(year=d.year + 1, month=1, day=7)
        else:
            end_date = pd.Timestamp(year=d.year, month=d.month + 1, day=7)

    else:
        end_date = pd.Timestamp(year=d.year, month=d.month, day=7)

        if d.month == 1:
            start_date = pd.Timestamp(year=d.year - 1, month=12, day=8)
        else:
            start_date = pd.Timestamp(year=d.year, month=d.month - 1, day=8)

    return start_date, end_date


def normalize_rule(value):
    rule = str(value or "").strip().lower()

    if rule in ["", "nan", "none", "arrival", "normal"]:
        return "normal"

    if rule in ["saturday", "saturday_work", "sat_work", "دوام السبت"]:
        return "saturday_work"

    if rule in ["no_absence", "no absence", "بدون غياب"]:
        return "no_absence"

    if rule in ["exempt", "استثناء", "مستثنى"]:
        return "exempt"

    if rule in ["daily_hours", "daily hours", "hours"]:
        return "daily_hours"

    return rule


def get_attendance_rule(emp_row):
    return normalize_rule(
        emp_row.get(
            "attendance_calculation",
            "normal"
        )
    )


def is_workday(day, attendance_rule="normal"):
    weekday = day.day_name()

    if weekday == "Friday":
        return False

    if weekday == "Saturday":
        return attendance_rule == "saturday_work"

    return True


def prepare_leaves(period_start, period_end):
    leaves = load_leaves_db()

    if leaves is None or leaves.empty:
        return pd.DataFrame()

    leaves = leaves.copy()

    for c in [
        "employee_id",
        "employee_no",
        "leave_type",
        "status",
        "name_ar",
        "department",
        "job_title",
        "notes",
        "attachment_name",
        "attachment_path",
    ]:
        if c not in leaves.columns:
            leaves[c] = ""

    leaves["employee_id"] = leaves["employee_id"].apply(normalize_id)
    leaves["employee_no"] = leaves["employee_no"].apply(normalize_id)

    leaves["start_date"] = pd.to_datetime(
        leaves["start_date"],
        errors="coerce"
    ).dt.normalize()

    leaves["end_date"] = pd.to_datetime(
        leaves["end_date"],
        errors="coerce"
    ).dt.normalize()

    leaves = leaves.dropna(
        subset=["employee_id", "start_date", "end_date"]
    ).copy()

    leaves["status_clean"] = (
        leaves["status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    approved_values = [
        "",
        "nan",
        "معتمدة",
        "معتمد",
        "approved",
        "active",
    ]

    leaves = leaves[
        leaves["status_clean"].isin(approved_values)
    ].copy()

    leaves = leaves[
        (leaves["end_date"] >= period_start)
        &
        (leaves["start_date"] <= period_end)
    ].copy()

    return leaves


def find_leave_for_day(leaves_df, employee_id, day):
    if leaves_df is None or leaves_df.empty:
        return False, ""

    emp_id = normalize_id(employee_id)

    check_date = pd.to_datetime(day).normalize()

    emp_leaves = leaves_df[
        leaves_df["employee_id"] == emp_id
    ].copy()

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
        hit.iloc[0].get("leave_type", "إجازة")
    ).strip()

    if not leave_type or leave_type.lower() == "nan":
        leave_type = "إجازة"

    return True, leave_type


def process_attendance(
    uploaded_file,
    work_start="08:00",
    grace_minutes=15,
    employees_df=None
):

    if uploaded_file is None:
        return pd.DataFrame()

    raw = pd.read_excel(
        uploaded_file,
        header=None
    )

    header_row = None

    for i in range(min(10, len(raw))):
        row_values = [
            str(x).strip().lower()
            for x in raw.iloc[i].tolist()
        ]

        if "employee id" in row_values and "date" in row_values:
            header_row = i
            break

    if header_row is None:
        raise Exception("لم يتم العثور على صف العناوين")

    df = pd.read_excel(
        uploaded_file,
        header=header_row
    )

    if df.empty:
        raise Exception("ملف البصمة فارغ")

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    employee_id_col = find_column(
        df,
        ["Employee ID", "employee_id"]
    )

    employee_name_col = find_column(
        df,
        ["First Name", "Employee Name", "Name"]
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

    missing = []

    if employee_id_col is None:
        missing.append("Employee ID")

    if date_col is None:
        missing.append("Date")

    if first_punch_col is None:
        missing.append("First Punch")

    if last_punch_col is None:
        missing.append("Last Punch")

    if missing:
        raise Exception(f"الأعمدة غير موجودة: {missing}")

    rename_map = {
        employee_id_col: "employee_id",
        date_col: "date",
        first_punch_col: "first_punch",
        last_punch_col: "last_punch",
    }

    if employee_name_col:
        rename_map[employee_name_col] = "employee_name"

    if department_col:
        rename_map[department_col] = "department"

    df.rename(
        columns=rename_map,
        inplace=True
    )

    if "employee_name" not in df.columns:
        df["employee_name"] = ""

    if "department" not in df.columns:
        df["department"] = ""

    df["employee_id"] = df["employee_id"].apply(normalize_id)

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    ).dt.normalize()

    df["first_punch"] = parse_time_col(
        df["first_punch"]
    )

    df["last_punch"] = parse_time_col(
        df["last_punch"]
    )

    df = df.dropna(
        subset=[
            "employee_id",
            "date"
        ]
    ).copy()

    if df.empty:
        return pd.DataFrame()

    df = (
        df.groupby(
            [
                "employee_id",
                "employee_name",
                "department",
                "date"
            ],
            as_index=False
        )
        .agg(
            first_punch=("first_punch", "min"),
            last_punch=("last_punch", "max"),
        )
    )

    if employees_df is not None and not employees_df.empty:
        emp = employees_df.copy()

        emp = emp.rename(columns={
            "Personnel Number": "employee_id",
            "Employee ID": "employee_id",
            "employee_id": "employee_id",
            "Arabic name": "employee_name",
            "Name": "name_en",
            "Search name": "search_name",
            "Section | Department": "department",
            "Contrac Profession": "job_title",
            "Nationality": "nationality",
            "attendance_calculation": "attendance_calculation",
        })

        if "attendance_calculation" not in emp.columns:
            emp["attendance_calculation"] = "normal"

        if "employee_name" not in emp.columns:
            emp["employee_name"] = ""

        if "department" not in emp.columns:
            emp["department"] = ""

        emp["employee_id"] = emp["employee_id"].apply(normalize_id)

        keep_cols = [
            "employee_id",
            "employee_name",
            "department",
            "attendance_calculation",
        ]

        emp = emp[keep_cols].drop_duplicates()

        df = df.merge(
            emp,
            on="employee_id",
            how="left",
            suffixes=("", "_emp")
        )

        df["employee_name"] = df["employee_name_emp"].fillna(
            df["employee_name"]
        )

        df["department"] = df["department_emp"].fillna(
            df["department"]
        )

        df.drop(
            columns=[
                c for c in ["employee_name_emp", "department_emp"]
                if c in df.columns
            ],
            inplace=True
        )

    if "attendance_calculation" not in df.columns:
        df["attendance_calculation"] = "normal"

    df["attendance_calculation"] = df[
        "attendance_calculation"
    ].apply(normalize_rule)

    period_start, period_end = get_attendance_period(
        df["date"].min()
    )

    df = df[
        (df["date"] >= period_start)
        &
        (df["date"] <= period_end)
    ].copy()

    leaves_df = prepare_leaves(
        period_start,
        period_end
    )

    start_hour = int(work_start.split(":")[0])
    start_minute = int(work_start.split(":")[1])

    start_minutes = start_hour * 60 + start_minute
    late_limit_minutes = int(start_minutes) + int(float(grace_minutes))

    end_minutes = int(17 * 60)

    def calc_late(row):
        if str(row.get("attendance_calculation", "")).lower() == "exempt":
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
            int(actual - late_limit_minutes)
        )

    def calc_early_leave(row):
        if pd.isna(row["last_punch"]):
            return 0

        actual = (
            row["last_punch"].hour * 60
            +
            row["last_punch"].minute
        )

        return max(
            0,
            int(end_minutes - actual)
        )

    def calc_overtime(row):
        if pd.isna(row["last_punch"]):
            return 0

        actual = (
            row["last_punch"].hour * 60
            +
            row["last_punch"].minute
        )

        return max(
            0,
            int(actual - end_minutes)
        )

    def calc_work_minutes(row):
        if pd.isna(row["first_punch"]):
            return 0

        if pd.isna(row["last_punch"]):
            return 0

        diff = row["last_punch"] - row["first_punch"]

        return max(
            0,
            int(diff.total_seconds() // 60)
        )

    df["weekday"] = df["date"].dt.day_name()
    df["weekday_ar"] = df["weekday"].map(WEEKDAY_AR)

    df["late_minutes"] = df.apply(
        calc_late,
        axis=1
    )

    df["early_leave_minutes"] = df.apply(
        calc_early_leave,
        axis=1
    )

    df["overtime_minutes"] = df.apply(
        calc_overtime,
        axis=1
    )

    df["worked_minutes"] = df.apply(
        calc_work_minutes,
        axis=1
    )

    df["work_hours"] = df["worked_minutes"].apply(
        minutes_to_hhmm
    )

    df["late_hhmm"] = df["late_minutes"].apply(
        minutes_to_hhmm
    )

    df["early_leave_hhmm"] = df["early_leave_minutes"].apply(
        minutes_to_hhmm
    )

    df["overtime_hhmm"] = df["overtime_minutes"].apply(
        minutes_to_hhmm
    )

    df["leave_type"] = ""

    df["status"] = df["late_minutes"].apply(
        lambda x: "متأخر" if x > 0 else "حاضر"
    )

    all_days = pd.date_range(
        start=pd.to_datetime(period_start),
        end=pd.to_datetime(period_end),
        freq="D"
    )

    employees = df[
        [
            "employee_id",
            "employee_name",
            "department",
            "attendance_calculation",
        ]
    ].drop_duplicates()

    final_rows = []

    for _, emp in employees.iterrows():

        emp_id = normalize_id(
            emp["employee_id"]
        )

        attendance_rule = get_attendance_rule(
            emp
        )

        emp_df = df[
            df["employee_id"].apply(normalize_id) == emp_id
        ].copy()

        for day in all_days:

            if not is_workday(
                day,
                attendance_rule
            ):
                continue

            existing = emp_df[
                emp_df["date"].dt.date == day.date()
            ]

            if not existing.empty:

                final_rows.append(
                    existing.iloc[0].to_dict()
                )

            else:

                if attendance_rule == "no_absence":
                    continue

                is_leave, leave_type = find_leave_for_day(
                    leaves_df,
                    emp_id,
                    day
                )

                weekday = day.day_name()

                final_rows.append({
                    "employee_id": emp_id,
                    "employee_name": emp["employee_name"],
                    "department": emp["department"],
                    "attendance_calculation": attendance_rule,
                    "date": day,
                    "weekday": weekday,
                    "weekday_ar": WEEKDAY_AR.get(weekday, weekday),
                    "first_punch": pd.NaT,
                    "last_punch": pd.NaT,
                    "worked_minutes": 0,
                    "work_hours": "00:00",
                    "late_minutes": 0,
                    "early_leave_minutes": 0,
                    "overtime_minutes": 0,
                    "late_hhmm": "00:00",
                    "early_leave_hhmm": "00:00",
                    "overtime_hhmm": "00:00",
                    "leave_type": leave_type,
                    "status": "إجازة" if is_leave else "غائب",
                })

    final_df = pd.DataFrame(final_rows)

    if final_df.empty:
        return final_df

    final_df = final_df.sort_values(
        [
            "date",
            "employee_id"
        ],
        ascending=[
            True,
            True
        ]
    ).reset_index(drop=True)

    return final_df