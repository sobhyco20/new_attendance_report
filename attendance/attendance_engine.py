import pandas as pd

from database.leaves_db import load_leaves_db


# =========================================================
# WEEKDAYS
# =========================================================

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
# MINUTES TO HHMM
# =========================================================

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
# PERIOD
# =========================================================

def get_attendance_period(any_date):

    d = pd.to_datetime(any_date)

    if d.day >= 8:

        start_date = pd.Timestamp(
            year=d.year,
            month=d.month,
            day=8
        )

        if d.month == 12:

            end_date = pd.Timestamp(
                year=d.year + 1,
                month=1,
                day=7
            )

        else:

            end_date = pd.Timestamp(
                year=d.year,
                month=d.month + 1,
                day=7
            )

    else:

        end_date = pd.Timestamp(
            year=d.year,
            month=d.month,
            day=7
        )

        if d.month == 1:

            start_date = pd.Timestamp(
                year=d.year - 1,
                month=12,
                day=8
            )

        else:

            start_date = pd.Timestamp(
                year=d.year,
                month=d.month - 1,
                day=8
            )

    return start_date, end_date


# =========================================================
# RULES
# =========================================================

def normalize_rule(value):

    rule = str(value or "").strip().lower()

    if rule in ["", "nan", "none", "arrival", "normal"]:

        return "normal"

    if rule in [
        "saturday",
        "saturday_work",
        "sat_work",
        "دوام السبت"
    ]:

        return "saturday_work"

    if rule in [
        "no_absence",
        "no absence",
        "بدون غياب"
    ]:

        return "no_absence"

    if rule in [
        "exempt",
        "استثناء",
        "مستثنى"
    ]:

        return "exempt"

    return "normal"


def get_attendance_rule(emp_row):

    return normalize_rule(
        emp_row.get(
            "attendance_calculation",
            "normal"
        )
    )


# =========================================================
# WORKDAY
# =========================================================

# =========================================================
# WORKDAY
# =========================================================

def is_workday(
    day,
    attendance_rule="normal",
    nationality=""
):

    weekday = day.day_name()

    nationality = str(
        nationality or ""
    ).strip().lower()

    # =====================================================
    # FRIDAY
    # =====================================================

    if weekday == "Friday":

        return False

    # =====================================================
    # SATURDAY
    # =====================================================

    if weekday == "Saturday":

        # السعودي إجازة السبت
        if nationality in [

            "saudi",

            "saudi arabia",

            "سعودي",

            "السعودية"
        ]:

            return False

        # غير السعودي يعمل السبت
        return True

    # =====================================================
    # NORMAL DAYS
    # =====================================================

    return True
# =========================================================
# LEAVES
# =========================================================

def prepare_leaves(period_start, period_end):

    leaves = load_leaves_db()

    if leaves is None or leaves.empty:

        return pd.DataFrame()

    leaves = leaves.copy()

    # أعمدة افتراضية
    for c in [
        "employee_id",
        "leave_type",
        "status",
    ]:

        if c not in leaves.columns:

            leaves[c] = ""

    leaves["employee_id"] = (
        leaves["employee_id"]
        .apply(normalize_id)
    )

    leaves["start_date"] = pd.to_datetime(
        leaves["start_date"],
        errors="coerce"
    ).dt.normalize()

    leaves["end_date"] = pd.to_datetime(
        leaves["end_date"],
        errors="coerce"
    ).dt.normalize()

    # المعتمد فقط
    leaves["status"] = (
        leaves["status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    approved_values = [

        "",

        "approved",

        "معتمد",

        "معتمدة",

        "active",
    ]

    leaves = leaves[
        leaves["status"].isin(
            approved_values
        )
    ].copy()

    # داخل الفترة
    leaves = leaves[
        (leaves["end_date"] >= period_start)
        &
        (leaves["start_date"] <= period_end)
    ].copy()

    return leaves


def find_leave_for_day(
    leaves_df,
    employee_id,
    day
):

    if leaves_df is None or leaves_df.empty:

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
    ).strip()

    if not leave_type:

        leave_type = "إجازة"

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
    # READ RAW
    # =====================================================

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

        if (
            "employee id" in row_values
            and
            "date" in row_values
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
    # COLUMNS
    # =====================================================

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

    rename_map = {

        employee_id_col: "employee_id",

        date_col: "date",

        first_punch_col: "first_punch",

        last_punch_col: "last_punch",
    }

    if employee_name_col:

        rename_map[
            employee_name_col
        ] = "employee_name"

    if department_col:

        rename_map[
            department_col
        ] = "department"

    df.rename(
        columns=rename_map,
        inplace=True
    )

    # =====================================================
    # DEFAULTS
    # =====================================================

    if "employee_name" not in df.columns:

        df["employee_name"] = ""

    if "department" not in df.columns:

        df["department"] = ""

    if "nationality" not in df.columns:

    df["nationality"] = ""

    # =====================================================
    # CLEAN
    # =====================================================

    df["employee_id"] = (
        df["employee_id"]
        .apply(normalize_id)
    )

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

    # =====================================================
    # GROUP
    # =====================================================

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

    # =====================================================
    # EMPLOYEES FILE
    # =====================================================

    if employees_df is not None and not employees_df.empty:

        emp = employees_df.copy()

        emp = emp.rename(columns={

            "Personnel Number": "employee_id",

            "Arabic name": "employee_name",

            "Section | Department": "department",
            "Nationality": "nationality",

            "attendance_calculation": "attendance_calculation",
        })

        emp["employee_id"] = (
            emp["employee_id"]
            .apply(normalize_id)
        )

        if "attendance_calculation" not in emp.columns:

            emp["attendance_calculation"] = "normal"

        keep_cols = [
        
            "employee_id",
        
            "employee_name",
        
            "department",
        
            "nationality",
        
            "attendance_calculation",
        ]

        emp = emp[
            keep_cols
        ].drop_duplicates()

        df = df.merge(
            emp,
            on="employee_id",
            how="left",
            suffixes=("", "_emp")
        )

        df["employee_name"] = (
            df["employee_name_emp"]
            .fillna(df["employee_name"])
        )

        df["department"] = (
            df["department_emp"]
            .fillna(df["department"])
        )

        df["nationality"] = (
            df["nationality_emp"]
            .fillna(df["nationality"])
        )
    

    # =====================================================
    # RULES
    # =====================================================

    if "attendance_calculation" not in df.columns:

        df["attendance_calculation"] = "normal"

    df["attendance_calculation"] = (
        df["attendance_calculation"]
        .apply(normalize_rule)
    )

    # =====================================================
    # PERIOD
    # =====================================================

    period_start, period_end = (
        get_attendance_period(
            df["date"].min()
        )
    )

    leaves_df = prepare_leaves(
        period_start,
        period_end
    )

    # =====================================================
    # TIME SETTINGS
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
        int(float(grace_minutes))
    )

    end_minutes = 17 * 60

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
    # LATE
    # =====================================================

    def calc_late(row):

        weekday = str(
            row.get("weekday", "")
        )

        # السبت بدون تأخير
        if weekday == "Saturday":

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

    # =====================================================
    # EARLY LEAVE
    # =====================================================

    def calc_early_leave(row):

        weekday = str(
            row.get("weekday", "")
        )

        # السبت بدون خروج مبكر
        if weekday == "Saturday":

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
            int(end_minutes - actual)
        )

    # =====================================================
    # OVERTIME
    # =====================================================

    def calc_overtime(row):

        weekday = str(
            row.get("weekday", "")
        )

        # السبت بدون إضافي
        if weekday == "Saturday":

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
            int(actual - end_minutes)
            )
        
    # =====================================================
    # WORK HOURS
    # =====================================================
    
    def calc_work_minutes(row):
    
        weekday = str(
            row.get("weekday", "")
        )
    
        # =================================================
        # SATURDAY
        # =================================================
    
        # السبت بدون ساعات
        if weekday == "Saturday":
    
            return 0
    
        # =================================================
        # NO PUNCH
        # =================================================
    
        if pd.isna(row["first_punch"]):
    
            return 0
    
        if pd.isna(row["last_punch"]):
    
            return 0
    
        # =================================================
        # CALC
        # =================================================
    
        diff = (
            row["last_punch"]
            -
            row["first_punch"]
        )
    
        minutes = int(
            diff.total_seconds() // 60
        )
    
        return max(0, minutes)
    # =====================================================
    # CALCULATIONS
    # =====================================================

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

    # =====================================================
    # FORMAT
    # =====================================================

    df["work_hours"] = (
        df["worked_minutes"]
        .apply(minutes_to_hhmm)
    )

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

    # =====================================================
    # STATUS
    # =====================================================

    def calc_status(row):

        weekday = str(
            row.get(
                "weekday",
                ""
            )
        ).strip()

        # السبت
        if weekday == "Saturday":

            if pd.isna(
                row.get("first_punch")
            ):

                return "غائب"

            return "حاضر"

        # الأيام العادية
        if row.get("late_minutes", 0) > 0:

            return "متأخر"

        return "حاضر"

    df["status"] = df.apply(
        calc_status,
        axis=1
    )

    df["leave_type"] = ""

    # =====================================================
    # ALL DAYS
    # =====================================================

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
            "nationality",
            "attendance_calculation",
        ]
    ].drop_duplicates()

    final_rows = []

    # =====================================================
    # LOOP
    # =====================================================

    for _, emp in employees.iterrows():

        emp_id = normalize_id(
            emp["employee_id"]
        )

        attendance_rule = (
            get_attendance_rule(emp)
        )

        emp_df = df[
            df["employee_id"]
            .apply(normalize_id) == emp_id
        ].copy()

        for day in all_days:
            
            if not is_workday(
            
                day,
            
                attendance_rule,
            
                emp.get("nationality", "")
            ):

                continue

            existing = emp_df[
                emp_df["date"].dt.date
                ==
                day.date()
            ]

            # يوجد حضور
            if not existing.empty:

                row_data = (
                    existing.iloc[0].to_dict()
                )

                # فحص الإجازة
                is_leave, leave_type = (
                    find_leave_for_day(
                        leaves_df,
                        emp_id,
                        day
                    )
                )

                
                if is_leave:
                
                    row_data["status"] = f"إجازة - {leave_type}"
                
                    row_data["leave_type"] = leave_type
                
                    # تصفير كل الحسابات
                    row_data["worked_minutes"] = 0
                
                    row_data["work_hours"] = "00:00"
                
                    row_data["late_minutes"] = 0
                
                    row_data["early_leave_minutes"] = 0
                
                    row_data["overtime_minutes"] = 0
                
                    row_data["late_hhmm"] = "00:00"
                
                    row_data["early_leave_hhmm"] = "00:00"
                
                    row_data["overtime_hhmm"] = "00:00"

                final_rows.append(
                    row_data
                )

            # لا يوجد حضور
            else:

                if attendance_rule == "no_absence":

                    continue

                is_leave, leave_type = (
                    find_leave_for_day(
                        leaves_df,
                        emp_id,
                        day
                    )
                )

                weekday = day.day_name()

                final_rows.append({

                    "employee_id": emp_id,

                    "employee_name": emp["employee_name"],

                    "department": emp["department"],

                    "attendance_calculation": attendance_rule,

                    "date": day,

                    "weekday": weekday,

                    "weekday_ar": WEEKDAY_AR.get(
                        weekday,
                        weekday
                    ),

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

                    "status": (
                        f"إجازة - {leave_type}"
                        if is_leave
                        else "غائب"
                    ),
                })

    # =====================================================
    # FINAL
    # =====================================================

    final_df = pd.DataFrame(
        final_rows
    )

    if final_df.empty:

        return final_df

    final_df = final_df.sort_values(
        [
            "date",
            "employee_id"
        ]
    ).reset_index(drop=True)

    return final_df
