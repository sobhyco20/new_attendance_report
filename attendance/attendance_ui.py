import pandas as pd
import streamlit as st

from datetime import time
from io import BytesIO

from attendance.attendance_engine import (
    process_attendance
)

from attendance.attendance_pdf import (
    build_attendance_pdf
)

# =========================================================
# UI
# =========================================================

def render_attendance_tab(employees_df=None):

    st.markdown(
        """
        <div class="card">
        <div class="card-title">
        📊 تقرير الحضور والانصراف
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # UPLOAD
    # =====================================================

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

    # =====================================================
    # PROCESS
    # =====================================================

    if process_btn:

        if uploaded_file is None:

            st.error(
                "ارفع ملف البصمة أولاً"
            )

            return

        try:

            df = process_attendance(

                uploaded_file,

                work_start=work_start.strftime(
                    "%H:%M"
                ),

                grace_minutes=grace,

                employees_df=employees_df
            )

            if df.empty:

                st.warning(
                    "لا توجد بيانات"
                )

                return

            # =================================================
            # COUNTS
            # =================================================

            present_df = df[
                df["status"].isin(
                    ["حاضر", "متأخر"]
                )
            ]

            absent_df = df[
                df["status"] == "غائب"
            ]

            leave_df = df[
                df["status"] == "إجازة"
            ]

            no_punch_df = df[
                (
                    df["first_punch"].isna()
                )
                &
                (
                    df["status"] != "إجازة"
                )
            ]

            # =================================================
            # KPI
            # =================================================

            total_days = len(df)

            total_present = len(
                present_df
            )

            total_absent = len(
                absent_df
            )

            total_leave = len(
                leave_df
            )

            total_no_punch = len(
                no_punch_df
            )

            total_late = int(
                df["late_minutes"].sum()
            )

            total_overtime = int(
                df["overtime_minutes"].sum()
            )

            total_early = int(
                df["early_leave_minutes"].sum()
            )

            total_worked = int(
                df["worked_minutes"].sum()
            )

            # =================================================
            # HEADER
            # =================================================

            st.markdown(
                """
                <div class="card">
                <div class="card-title">
                📈 ملخص التقرير
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # KPI ROW 1
            # =================================================

            k1, k2, k3, k4, k5 = st.columns(5)

            k1.metric(
                "📅 إجمالي الأيام",
                total_days
            )

            k2.metric(
                "✅ الحضور",
                total_present
            )

            k3.metric(
                "❌ الغياب",
                total_absent
            )

            k4.metric(
                "🏖 الإجازات",
                total_leave
            )

            k5.metric(
                "⚠ بدون بصمة",
                total_no_punch
            )

            # =================================================
            # KPI ROW 2
            # =================================================

            k6, k7, k8, k9 = st.columns(4)

            k6.metric(
                "⏰ التأخير",
                f"{total_late} دقيقة"
            )

            k7.metric(
                "🚪 الخروج المبكر",
                f"{total_early} دقيقة"
            )

            k8.metric(
                "➕ الإضافي",
                f"{total_overtime} دقيقة"
            )

            k9.metric(
                "🕒 ساعات العمل",
                round(total_worked / 60, 2)
            )

            # =================================================
            # TABS
            # =================================================

            tab1, tab2, tab3, tab4 = st.tabs([

                "✅ الحضور",

                "❌ الغياب",

                "🏖 الإجازات",

                "⚠ بدون بصمة"
            ])

            # =================================================
            # PRESENT
            # =================================================

            with tab1:

                if present_df.empty:

                    st.info(
                        "لا توجد بيانات حضور"
                    )

                else:

                    st.dataframe(

                        present_df[
                            [
                                "employee_id",
                                "employee_name",
                                "date",
                                "weekday_ar",
                                "first_punch",
                                "last_punch",
                                "late_hhmm",
                                "overtime_hhmm",
                                "status"
                            ]
                        ],

                        use_container_width=True
                    )

            # =================================================
            # ABSENT
            # =================================================

            with tab2:

                if absent_df.empty:

                    st.success(
                        "لا يوجد غياب"
                    )

                else:

                    st.dataframe(

                        absent_df[
                            [
                                "employee_id",
                                "employee_name",
                                "date",
                                "weekday_ar",
                                "status"
                            ]
                        ],

                        use_container_width=True
                    )

            # =================================================
            # LEAVES
            # =================================================

            with tab3:

                if leave_df.empty:

                    st.info(
                        "لا توجد إجازات"
                    )

                else:

                    st.dataframe(

                        leave_df[
                            [
                                "employee_id",
                                "employee_name",
                                "date",
                                "weekday_ar",
                                "leave_type",
                                "status"
                            ]
                        ],

                        use_container_width=True
                    )

            # =================================================
            # NO PUNCH
            # =================================================

            with tab4:

                if no_punch_df.empty:

                    st.success(
                        "لا توجد أيام بدون بصمة"
                    )

                else:

                    st.dataframe(

                        no_punch_df[
                            [
                                "employee_id",
                                "employee_name",
                                "date",
                                "weekday_ar",
                                "status"
                            ]
                        ],

                        use_container_width=True
                    )

            # =================================================
            # DOWNLOAD
            # =================================================

            st.markdown(
                """
                <div class="card">
                <div class="card-title">
                📥 التصدير
                </div>
                """,
                unsafe_allow_html=True
            )

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

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                f"حدث خطأ أثناء معالجة الملف: {e}"
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )