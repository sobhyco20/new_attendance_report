import pandas as pd
import streamlit as st

from io import BytesIO

from leaves.leaves_helpers import (

    safe_str,
    fmt_date,

    normalize_emp_id,

    employee_option_label,

    find_employee_record,

    save_leave_attachment
)

from leaves.leaves_services import (

    load_leaves,

    add_leave_record,

    edit_leave_record,

    remove_leave_record
)

from leaves.leaves_pdf import (
    build_leaves_pdf
)

# =========================================================
# DEMO EMPLOYEES
# =========================================================
# لاحقًا سيتم استبداله بملف الموظفين الحقيقي

# =========================================================
# LOAD EMPLOYEES
# =========================================================

# =========================================================
# LOAD EMPLOYEES
# =========================================================

def load_employees():

    try:

        path = "data/employees.xlsx"

        df = pd.read_excel(path)

        # =============================================
        # CLEAN COLUMNS
        # =============================================

        df.columns = [

            str(c).strip()

            for c in df.columns
        ]

        # =============================================
        # RENAME REAL COLUMNS
        # =============================================

        rename_map = {

            "employee_id": "employee_id",

            "Name": "name_en",

            "Arabic name": "name_ar",

            "Section | Department": "department",

            "Contrac Profession": "job_title",
        }

        df.rename(
            columns=rename_map,
            inplace=True
        )

        # =============================================
        # REQUIRED
        # =============================================

        required = [

            "employee_id",

            "name_ar"
        ]

        for c in required:

            if c not in df.columns:

                raise Exception(
                    f"العمود غير موجود: {c}"
                )

        # =============================================
        # DEFAULTS
        # =============================================

        if "name_en" not in df.columns:
            df["name_en"] = ""

        if "department" not in df.columns:
            df["department"] = ""

        if "job_title" not in df.columns:
            df["job_title"] = ""

        # =============================================
        # EMPLOYEE NO
        # =============================================

        df["employee_no"] = df[
            "employee_id"
        ]

        # =============================================
        # IDS
        # =============================================

        df["employee_id"] = (

            df["employee_id"]

            .astype(str)

            .str.replace(".0", "")

            .str.strip()
        )

        df["employee_no"] = (

            df["employee_no"]

            .astype(str)

            .str.replace(".0", "")

            .str.strip()
        )

        # =============================================
        # REMOVE EMPTY
        # =============================================

        df = df[
            df["employee_id"] != ""
        ]

        return df

    except Exception as e:

        st.error(
            f"خطأ في ملف الموظفين: {e}"
        )

        return pd.DataFrame()




# =========================================================
# TABLE
# =========================================================

def render_leave_results_table(df):

    show_df = df.copy()

    cols = [

        "employee_no",
        "name_ar",

        "department",

        "leave_type",

        "start_date",
        "end_date",

        "status",

        "notes"
    ]

    cols = [
        c for c in cols
        if c in show_df.columns
    ]

    show_df = show_df[cols]

    rename_map = {

        "employee_no": "الرقم الوظيفي",

        "name_ar": "اسم الموظف",

        "department": "القسم",

        "leave_type": "نوع الإجازة",

        "start_date": "من تاريخ",

        "end_date": "إلى تاريخ",

        "status": "الحالة",

        "notes": "ملاحظات"
    }

    show_df.rename(
        columns=rename_map,
        inplace=True
    )

    st.dataframe(
        show_df,
        use_container_width=True
    )


# =========================================================
# MAIN UI
# =========================================================

def render_leaves_tab():

    employees_df = load_employees()

    employee_lookup = employees_df.copy()

    # =====================================================
    # OPTIONS
    # =====================================================

    options_map = {

        employee_option_label(r):

            normalize_emp_id(
                r.get("employee_id")
            )

        for _, r in employee_lookup.iterrows()
    }

    # =====================================================
    # TABS
    # =====================================================

    register_tab, view_tab, edit_tab = st.tabs([

        "➕ تسجيل إجازة",

        "📊 عرض الإجازات",

        "✏️ تعديل الإجازات"
    ])

    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.markdown(
            """
            <div class="card">
            <div class="card-title">
            ➕ تسجيل إجازة جديدة
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # MANUAL
        # =================================================

        st.markdown(
            "### ➕ تسجيل إجازة يدوية"
        )

        with st.form(
            "leave_form",
            clear_on_submit=True
        ):

            selected_label = st.selectbox(

                "الموظف",

                options=list(options_map.keys()),

                index=None,

                placeholder="ابحث باسم الموظف..."
            )

            leave_type = st.selectbox(

                "نوع الإجازة",

                [
                    "سنوية",
                    "مرضية",
                    "بدون راتب",
                    "اضطرارية",
                    "رسمية",
                    "أخرى"
                ]
            )

            c1, c2 = st.columns(2)

            with c1:

                leave_start = st.date_input(
                    "من تاريخ"
                )

            with c2:

                leave_end = st.date_input(
                    "إلى تاريخ"
                )

            notes = st.text_area(
                "ملاحظات"
            )

            leave_file = st.file_uploader(

                "إرفاق ملف الإجازة",

                type=[
                    "pdf",
                    "png",
                    "jpg",
                    "jpeg",
                    "doc",
                    "docx"
                ]
            )

            submitted = st.form_submit_button(
                "💾 حفظ الإجازة"
            )

        # =================================================
        # SAVE
        # =================================================

        if submitted:

            if not selected_label:

                st.error(
                    "اختر الموظف أولاً"
                )

            elif leave_end < leave_start:

                st.error(
                    "تاريخ النهاية يجب أن يكون بعد البداية"
                )

            else:

                emp_key = options_map[
                    selected_label
                ]

                emp = find_employee_record(
                    employees_df,
                    emp_key
                )

                if not emp:

                    st.error(
                        "الموظف غير موجود"
                    )

                else:

                    emp_id = normalize_emp_id(
                        emp.get("employee_id")
                    )

                    attachment_name, attachment_path = (
                        save_leave_attachment(

                            leave_file,

                            emp_id,

                            leave_start,

                            leave_end
                        )
                    )

                    add_leave_record({

                        "leave_id":

                            f"LV-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S%f')}",

                        "employee_id":
                            emp_id,

                        "employee_no":
                            normalize_emp_id(
                                emp.get("employee_no")
                            ),

                        "name_ar":
                            safe_str(
                                emp.get("name_ar")
                            ),

                        "name_en":
                            safe_str(
                                emp.get("name_en")
                            ),

                        "department":
                            safe_str(
                                emp.get("department")
                            ),

                        "job_title":
                            safe_str(
                                emp.get("job_title")
                            ),

                        "leave_type":
                            leave_type,

                        "start_date":
                            pd.Timestamp(
                                leave_start
                            ),

                        "end_date":
                            pd.Timestamp(
                                leave_end
                            ),

                        "status":
                            "معتمدة",

                        "attachment_name":
                            attachment_name,

                        "attachment_path":
                            attachment_path,

                        "notes":
                            notes,

                        "created_at":
                            pd.Timestamp.now(),

                        "created_by":
                            st.session_state.get(
                                "login_user"
                            ),
                    })

                    st.success(
                        "✅ تم حفظ الإجازة"
                    )

                    st.rerun()

        # =================================================
        # SEPARATOR
        # =================================================

        st.markdown("<hr>", unsafe_allow_html=True)

        # =================================================
        # BULK IMPORT
        # =================================================

        st.markdown(
            "### 📥 رفع ملف إجازات"
        )

        st.caption(
            "هذا الاستخدام ثانوي عند رفع عدد كبير من الإجازات."
        )

        with st.form(
            "bulk_leave_form"
        ):

            bulk_file = st.file_uploader(

                "ارفع ملف Excel",

                type=["xlsx", "xls"]
            )

            bulk_submit = st.form_submit_button(
                "📥 استيراد الملف"
            )

        if bulk_submit:

            if bulk_file is None:

                st.error(
                    "اختر ملف Excel أولاً"
                )

            else:

                try:

                    bulk_df = pd.read_excel(
                        bulk_file
                    )

                    required_cols = [

                        "employee_id",

                        "leave_type",

                        "start_date",

                        "end_date"
                    ]

                    missing = [

                        c for c in required_cols

                        if c not in bulk_df.columns
                    ]

                    if missing:

                        st.error(
                            f"الأعمدة الناقصة: {missing}"
                        )

                    else:

                        bulk_df["start_date"] = (
                            pd.to_datetime(

                                bulk_df["start_date"],

                                errors="coerce"
                            )
                        )

                        bulk_df["end_date"] = (
                            pd.to_datetime(

                                bulk_df["end_date"],

                                errors="coerce"
                            )
                        )

                        inserted = 0

                        for _, r in bulk_df.iterrows():

                            emp_id = normalize_emp_id(
                                r.get("employee_id")
                            )

                            if not emp_id:
                                continue

                            emp = find_employee_record(
                                employees_df,
                                emp_id
                            )

                            if emp:

                                emp_no = normalize_emp_id(
                                    emp.get("employee_no")
                                )

                                name_ar = safe_str(
                                    emp.get("name_ar")
                                )

                                name_en = safe_str(
                                    emp.get("name_en")
                                )

                                department = safe_str(
                                    emp.get("department")
                                )

                                job_title = safe_str(
                                    emp.get("job_title")
                                )

                            else:

                                emp_no = emp_id

                                name_ar = ""

                                name_en = ""

                                department = ""

                                job_title = ""

                            add_leave_record({

                                "leave_id":

                                    f"LV-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S%f')}",

                                "employee_id":
                                    emp_id,

                                "employee_no":
                                    emp_no,

                                "name_ar":
                                    name_ar,

                                "name_en":
                                    name_en,

                                "department":
                                    department,

                                "job_title":
                                    job_title,

                                "leave_type":
                                    safe_str(
                                        r.get("leave_type")
                                    ),

                                "start_date":
                                    pd.Timestamp(
                                        r.get("start_date")
                                    ),

                                "end_date":
                                    pd.Timestamp(
                                        r.get("end_date")
                                    ),

                                "status":
                                    "معتمدة",

                                "attachment_name":
                                    "",

                                "attachment_path":
                                    "",

                                "notes":
                                    safe_str(
                                        r.get("notes")
                                    ),

                                "created_at":
                                    pd.Timestamp.now(),

                                "created_by":
                                    st.session_state.get(
                                        "login_user"
                                    ),
                            })

                            inserted += 1

                        st.success(
                            f"✅ تم رفع {inserted} إجازة"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(e)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # VIEW
    # =====================================================

    with view_tab:

        st.markdown(
            """
            <div class="card">
            <div class="card-title">
            📊 عرض الإجازات
            </div>
            """,
            unsafe_allow_html=True
        )

        df = load_leaves()

        # =================================================
        # KPIS
        # =================================================

        k1, k2, k3 = st.columns(3)

        k1.metric(
            "عدد الإجازات",
            len(df)
        )

        k2.metric(
            "عدد الموظفين",
            df["employee_id"].nunique()
            if not df.empty else 0
        )

        k3.metric(
            "الإجازات المعتمدة",
            len(
                df[
                    df["status"] == "معتمدة"
                ]
            ) if not df.empty else 0
        )

        st.markdown("### 🔎 الفلاتر")

        view_mode = st.radio(

            "نوع العرض",

            [
                "كل الموظفين",
                "موظف محدد"
            ],

            horizontal=True
        )

        c1, c2 = st.columns(2)

        with c1:

            report_from = st.date_input(
                "من تاريخ"
            )

        with c2:

            report_to = st.date_input(
                "إلى تاريخ"
            )

        selected_emp_key = ""

        if view_mode == "موظف محدد":

            selected_emp = st.selectbox(

                "اختر الموظف",

                options=list(options_map.keys()),

                index=None
            )

            if selected_emp:

                selected_emp_key = options_map[
                    selected_emp
                ]

        show_btn = st.button(
            "📄 عرض الإجازات",
            use_container_width=True
        )

        # =================================================
        # SHOW
        # =================================================

        if show_btn:

            if df.empty:

                st.info(
                    "لا توجد إجازات"
                )

            else:

                mask = (

                    (
                        df["start_date"]
                        <=
                        pd.to_datetime(report_to)
                    )

                    &

                    (
                        df["end_date"]
                        >=
                        pd.to_datetime(report_from)
                    )
                )

                filtered = df[
                    mask
                ].copy()

                if (

                    view_mode
                    ==
                    "موظف محدد"

                ):

                    filtered = filtered[

                        (
                            filtered["employee_id"]

                            ==

                            normalize_emp_id(
                                selected_emp_key
                            )
                        )

                    ]

                if filtered.empty:

                    st.warning(
                        "لا توجد نتائج"
                    )

                else:

                    st.success(
                        f"عدد النتائج: {len(filtered)}"
                    )

                    render_leave_results_table(
                        filtered
                    )

                    # =========================
                    # PDF
                    # =========================

                    pdf_bytes = build_leaves_pdf(
                        filtered
                    )

                    st.download_button(

                        "📄 تحميل PDF",

                        data=pdf_bytes,

                        file_name="leave_report.pdf",

                        mime="application/pdf",

                        use_container_width=True
                    )

                    # =========================
                    # EXCEL
                    # =========================

                    excel_buffer = BytesIO()

                    filtered.to_excel(
                        excel_buffer,
                        index=False
                    )

                    excel_buffer.seek(0)

                    st.download_button(

                        "📊 تحميل Excel",

                        data=excel_buffer,

                        file_name="leave_report.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                        use_container_width=True
                    )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # EDIT
    # =====================================================

    with edit_tab:

        st.markdown(
            """
            <div class="card">
            <div class="card-title">
            ✏️ تعديل الإجازات
            </div>
            """,
            unsafe_allow_html=True
        )

        df = load_leaves()

        if df.empty:

            st.info(
                "لا توجد إجازات"
            )

        else:

            df["option_label"] = df.apply(

                lambda r:

                f"{safe_str(r.get('name_ar'))} | "
                f"{fmt_date(r.get('start_date'))} | "
                f"{safe_str(r.get('leave_type'))}",

                axis=1
            )

            options = dict(zip(

                df["option_label"],

                df["leave_id"]
            ))

            selected_label = st.selectbox(

                "اختر سجل الإجازة",

                options=list(options.keys()),

                index=None
            )

            if selected_label:

                leave_id = options[
                    selected_label
                ]

                row = df[
                    df["leave_id"] == leave_id
                ]

                if not row.empty:

                    r = row.iloc[0]

                    with st.form(
                        "edit_leave_form"
                    ):

                        leave_types = [

                            "سنوية",

                            "مرضية",

                            "بدون راتب",

                            "اضطرارية",

                            "رسمية",

                            "أخرى"
                        ]

                        current_type = safe_str(
                            r.get("leave_type")
                        )

                        current_index = 0

                        if current_type in leave_types:

                            current_index = leave_types.index(
                                current_type
                            )

                        new_type = st.selectbox(

                            "نوع الإجازة",

                            leave_types,

                            index=current_index
                        )

                        c1, c2 = st.columns(2)

                        with c1:

                            new_start = st.date_input(

                                "من تاريخ",

                                value=pd.to_datetime(
                                    r.get("start_date")
                                ).date()
                            )

                        with c2:

                            new_end = st.date_input(

                                "إلى تاريخ",

                                value=pd.to_datetime(
                                    r.get("end_date")
                                ).date()
                            )

                        new_notes = st.text_area(

                            "ملاحظات",

                            value=safe_str(
                                r.get("notes")
                            )
                        )

                        save_btn = st.form_submit_button(
                            "💾 حفظ التعديل"
                        )

                    if save_btn:

                        edit_leave_record({

                            "leave_id":
                                leave_id,

                            "leave_type":
                                new_type,

                            "start_date":
                                pd.Timestamp(
                                    new_start
                                ),

                            "end_date":
                                pd.Timestamp(
                                    new_end
                                ),

                            "status":
                                "معتمدة",

                            "attachment_name":
                                safe_str(
                                    r.get("attachment_name")
                                ),

                            "attachment_path":
                                safe_str(
                                    r.get("attachment_path")
                                ),

                            "notes":
                                new_notes,
                        })

                        st.success(
                            "✅ تم تعديل الإجازة"
                        )

                        st.rerun()

                    # =========================
                    # DELETE
                    # =========================

                    if st.button(

                        "🗑️ حذف الإجازة",

                        use_container_width=True
                    ):

                        remove_leave_record(
                            leave_id
                        )

                        st.success(
                            "تم حذف الإجازة"
                        )

                        st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )