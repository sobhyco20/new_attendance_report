import pandas as pd
import streamlit as st

from datetime import time
from io import BytesIO

from attendance.attendance_engine import process_attendance
from attendance.attendance_pdf import build_attendance_pdf


def safe_sum(df, column):
    if column not in df.columns:
        return 0

    return int(
        pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0).sum()
    )


def safe_value(df, column, default=""):
    if column not in df.columns or df.empty:
        return default

    value = df[column].iloc[0]

    if pd.isna(value):
        return default

    return str(value)


def card(title, value, subtitle, icon):

    with st.container(border=True):

        st.markdown(
            f"""
            <h3 style="text-align:right; direction:rtl;">
                {icon} {title}
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h1 style="text-align:right; direction:rtl; font-size:48px;">
                {value}
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <p style="text-align:right; direction:rtl; color:#cbd5e1; font-size:18px;">
                {subtitle}
            </p>
            """,
            unsafe_allow_html=True
        )


def render_attendance_tab(employees_df=None):

    st.title("📈 ملخص التقرير")
    st.caption("عرض شامل للحضور والانصراف والإجازات")

    uploaded_file = st.file_uploader(
        "📄 ارفع ملف البصمة",
        type=["xlsx", "xls"]
    )

    c1, c2 = st.columns(2)

    with c1:
        work_start = st.time_input(
            "🕗 بداية الدوام",
            value=time(8, 0)
        )

    with c2:
        grace = st.number_input(
            "⏱ دقائق السماح",
            min_value=0,
            value=15
        )

    process_btn = st.button(
        "🚀 تشغيل التقرير",
        use_container_width=True
    )

    if not process_btn:
        return

    if uploaded_file is None:
        st.error("ارفع ملف البصمة أولاً")
        return

    try:

        df = process_attendance(
            uploaded_file,
            work_start=work_start.strftime("%H:%M"),
            grace_minutes=grace,
            employees_df=employees_df
        )

        if df.empty:
            st.warning("لا توجد بيانات")
            return

        present_df = df[
            df["status"].isin(["حاضر", "متأخر"])
        ]

        absent_df = df[
            df["status"] == "غائب"
        ]

        leave_df = df[
            df["status"] == "إجازة"
        ]

        if "first_punch" in df.columns:
            no_punch_df = df[
                df["first_punch"].isna()
                &
                (df["status"] != "إجازة")
            ]
        else:
            no_punch_df = pd.DataFrame()

        total_days = len(df)
        total_present = len(present_df)
        total_absent = len(absent_df)
        total_leave = len(leave_df)
        total_no_punch = len(no_punch_df)

        total_late = safe_sum(df, "late_minutes")
        total_overtime = safe_sum(df, "overtime_minutes")
        total_early = safe_sum(df, "early_leave_minutes")
        total_worked_minutes = safe_sum(df, "worked_minutes")
        total_worked_hours = round(total_worked_minutes / 60, 2)

        employee_id = safe_value(df, "employee_id", "")

        # =====================================================
        # EMPLOYEE NAME FROM EMPLOYEES FILE
        # =====================================================

        employee_name = ""

        try:

            if employees_df is not None:

                # تنظيف أسماء الأعمدة
                employees_df.columns = (
                    employees_df.columns
                    .astype(str)
                    .str.strip()
                )

                # رقم الموظف من ملف البصمة
                emp_id = str(employee_id).strip()

                # =================================================
                # اكتشاف عمود الرقم الوظيفي تلقائياً
                # =================================================

                emp_col = None

                possible_cols = [

                    "employee_id",

                    "Employee ID",

                    "Employee No",

                    "Emp No",

                    "Emp ID",

                    "ID",

                    "Code",

                    "Employee Code"
                ]

                for col in employees_df.columns:

                    if str(col).strip() in possible_cols:

                        emp_col = col

                        break

                # =================================================
                # البحث عن الموظف
                # =================================================

                if emp_col is not None:

                    employees_df[emp_col] = (
                        employees_df[emp_col]
                        .astype(str)
                        .str.strip()
                    )

                    emp_row = employees_df[
                        employees_df[emp_col] == emp_id
                    ]

                    if not emp_row.empty:

                        # الاسم العربي
                        if "Arabic name" in emp_row.columns:

                            employee_name = str(
                                emp_row.iloc[0]["Arabic name"]
                            )

        except Exception as ex:

            st.warning(
                f"خطأ في قراءة الاسم العربي: {ex}"
            )

        # fallback
        if not employee_name:

            employee_name = safe_value(
                df,
                "employee_name",
                ""
            )



        st.divider()

        st.subheader("👤 بيانات الموظف")

        e1, e2 = st.columns(2)

        with e1:
            card(
                "اسم الموظف",
                employee_name,
                "الاسم العربي / اسم الموظف",
                "👤"
            )

        with e2:
            card(
                "الرقم الوظيفي",
                employee_id,
                "رقم الموظف",
                "🪪"
            )

        st.divider()

        st.subheader("📊 ملخص الحالات")

        r1c1, r1c2, r1c3, r1c4 = st.columns(4)

        with r1c1:
            card("أيام العمل", total_days, "إجمالي أيام العمل", "📅")

        with r1c2:
            card("الحضور", total_present, "أيام الحضور", "✅")

        with r1c3:
            card("الغياب", total_absent, "أيام الغياب", "❌")

        with r1c4:
            card("الإجازات", total_leave, "أيام الإجازات", "🏖️")

        r2c1, r2c2, r2c3, r2c4 = st.columns(4)

        with r2c1:
            card("ساعات العمل", total_worked_hours, "إجمالي ساعات العمل", "🕒")

        with r2c2:
            card("الوقت الفعلي", total_worked_minutes, "إجمالي الوقت بالدقيقة", "⏱️")

        with r2c3:
            card("الخروج المبكر", total_early, "إجمالي الخروج المبكر بالدقيقة", "🚪")

        with r2c4:
            card("التأخير", total_late, "إجمالي التأخير بالدقيقة", "⏰")

        r3c1, r3c2 = st.columns(2)

        with r3c1:
            card("بدون بصمة", total_no_punch, "أيام بدون بصمة", "⚠️")

        with r3c2:
            card("الإضافي", total_overtime, "إجمالي الإضافي بالدقيقة", "➕")

        st.divider()

        st.subheader("📥 التصدير")

        pdf = build_attendance_pdf(df)

        excel_buffer = BytesIO()

        export_df = df.copy()

        export_df.to_excel(
            excel_buffer,
            index=False
        )

        excel_buffer.seek(0)

        d1, d2 = st.columns(2)

        with d1:
            st.download_button(
                "📄 تحميل PDF",
                data=pdf,
                file_name="attendance_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with d2:
            st.download_button(
                "📊 تحميل Excel",
                data=excel_buffer,
                file_name="attendance_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف: {e}")