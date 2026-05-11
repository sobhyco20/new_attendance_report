from io import BytesIO
import os

import pandas as pd
import arabic_reshaper

from bidi.algorithm import get_display

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =========================================================
# FONTS
# =========================================================

pdfmetrics.registerFont(
    TTFont(
        "Arabic",
        "fonts/Amiri-Regular.ttf"
    )
)

pdfmetrics.registerFont(
    TTFont(
        "ArabicBold",
        "fonts/Amiri-Bold.ttf"
    )
)

# =========================================================
# WEEK DAYS
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
# RTL
# =========================================================

def ar(text):

    if text is None:
        return ""

    text = str(text)

    reshaped = arabic_reshaper.reshape(text)

    return get_display(reshaped)

# =========================================================
# HELPERS
# =========================================================

def safe_str(v):

    if v is None:
        return ""

    try:

        if pd.isna(v):
            return ""

    except Exception:
        pass

    return str(v).strip()


def fmt_date(v):

    try:

        return pd.to_datetime(v).strftime(
            "%d-%m-%Y"
        )

    except Exception:

        return ""


def fmt_time(v):

    try:

        if pd.isna(v):
            return ""

        return pd.to_datetime(v).strftime(
            "%H:%M"
        )

    except Exception:

        return ""


def minutes_to_hhmm(minutes):

    try:

        minutes = int(minutes or 0)

        sign = "-" if minutes < 0 else ""

        minutes = abs(minutes)

        return f"{sign}{minutes // 60:02}:{minutes % 60:02}"

    except Exception:

        return "00:00"


def minutes_to_ar_text(minutes):

    try:

        minutes = int(minutes or 0)

        sign = "-" if minutes < 0 else ""

        minutes = abs(minutes)

        h = minutes // 60

        m = minutes % 60

        return f"{sign}{h} ساعة و {m} دقيقة"

    except Exception:

        return "0 ساعة و 0 دقيقة"


def month_title(df):

    try:

        d = pd.to_datetime(
            df["date"].dropna().max()
        )

        return f"تقرير الحضور والانصراف - {d.month:02d}/{d.year}"

    except Exception:

        return "تقرير الحضور والانصراف"

# =========================================================
# MAIN PDF
# =========================================================

def build_attendance_pdf(df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=28,
        leftMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # STYLES
    # =====================================================

    title_style = ParagraphStyle(
        "title",
        parent=styles["Normal"],
        fontName="ArabicBold",
        fontSize=18,
        alignment=1,
        leading=24,
        textColor=colors.HexColor("#0f172a")
    )

    name_style = ParagraphStyle(
        "name",
        parent=styles["Normal"],
        fontName="ArabicBold",
        fontSize=14,
        alignment=1,
        leading=20,
        textColor=colors.HexColor("#111827")
    )

    info_style = ParagraphStyle(
        "info",
        parent=styles["Normal"],
        fontName="Arabic",
        fontSize=9,
        alignment=1,
        leading=14,
    )

    section_style = ParagraphStyle(
        "section",
        parent=styles["Normal"],
        fontName="ArabicBold",
        fontSize=12,
        alignment=2,
        leading=18,
        textColor=colors.HexColor("#1d4ed8"),
        spaceBefore=10,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "normal",
        parent=styles["Normal"],
        fontName="Arabic",
        fontSize=9,
        alignment=2,
        leading=14,
    )

    total_style = ParagraphStyle(
        "total",
        parent=styles["Normal"],
        fontName="ArabicBold",
        fontSize=10,
        alignment=2,
        leading=16,
        textColor=colors.HexColor("#111827")
    )

    elements = []

    # =====================================================
    # EMPTY
    # =====================================================

    if df is None or df.empty:

        elements.append(
            Paragraph(
                ar("لا توجد بيانات"),
                title_style
            )
        )

        doc.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf

    # =====================================================
    # DATA
    # =====================================================

    data_df = df.copy()

    data_df["date"] = pd.to_datetime(
        data_df["date"],
        errors="coerce"
    )

    data_df = data_df.sort_values(
        "date"
    )

    first = data_df.iloc[0]

    employee_name = safe_str(
        first.get("employee_name_ar")
    )

    if not employee_name:

        employee_name = safe_str(
            first.get("employee_name")
        )

    employee_id = safe_str(
        first.get("employee_id")
    )

    department = safe_str(
        first.get("department")
    )

    job_title = safe_str(
        first.get("job_title")
    )

    nationality = safe_str(
        first.get("nationality")
    )

    title = month_title(
        data_df
    )

    # =====================================================
    # LOGO
    # =====================================================

    logo_path = os.path.join(
        os.getcwd(),
        "logos",
        "company_logo.png"
    )

    if os.path.exists(logo_path):

        try:

            logo = Image(
                logo_path,
                width=140,
                height=70
            )

            logo.hAlign = "CENTER"

            elements.append(logo)

            elements.append(
                Spacer(1, 12)
            )

        except Exception as ex:

            print("LOGO ERROR:", ex)

    else:

        print("LOGO NOT FOUND:", logo_path)

    # =====================================================
    # TITLES
    # =====================================================

    elements.append(
        Paragraph(
            ar(title),
            title_style
        )
    )

    elements.append(
        Spacer(1, 6)
    )

    elements.append(
        Paragraph(
            ar(employee_name),
            name_style
        )
    )

    # =====================================================
    # INFO
    # =====================================================

    info_parts = []

    if employee_id:

        info_parts.append(
            f"الرقم الوظيفي: {employee_id}"
        )

    if job_title:

        info_parts.append(
            f"الوظيفة: {job_title}"
        )

    if department:

        info_parts.append(
            f"الإدارة: {department}"
        )

    if nationality:

        info_parts.append(
            f"الجنسية: {nationality}"
        )

    if info_parts:

        elements.append(
            Paragraph(
                ar(" | ".join(info_parts)),
                info_style
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    # =====================================================
    # NOTE
    # =====================================================

    note = (
        "يتم احتساب التأخير بعد وقت الدوام "
        "والخروج المبكر قبل نهاية الدوام "
        "والإضافي بعد نهاية الدوام."
    )

    elements.append(
        Paragraph(
            ar(note),
            normal_style
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    # =====================================================
    # LATE SECTION
    # =====================================================

    elements.append(
        Paragraph(
            ar("أيام التأخير"),
            section_style
        )
    )

    late_df = data_df[

        (
            pd.to_numeric(
                data_df["late_minutes"],
                errors="coerce"
            ).fillna(0) > 0
        )

        &

        (
            data_df["weekday"] != "Saturday"
        )

        &

        (
            ~data_df["status"]
            .astype(str)
            .str.contains("إجازة")
        )
    ]

    if late_df.empty:

        elements.append(
            Paragraph(
                ar("لا توجد أيام بها تأخير"),
                normal_style
            )
        )

    else:

        table_data = [[

            ar("الحالة"),

            ar("الإضافي"),

            ar("الخروج المبكر"),

            ar("التأخير"),

            ar("ساعات العمل"),

            ar("آخر بصمة"),

            ar("أول بصمة"),

            ar("التاريخ"),

            ar("اليوم"),
        ]]

        for _, r in late_df.iterrows():

            day_en = safe_str(
                r.get("weekday")
            )

            day_ar = (
                safe_str(
                    r.get("weekday_ar")
                )
                or WEEKDAY_AR.get(
                    day_en,
                    day_en
                )
            )

            table_data.append([

                ar(
                    safe_str(
                        r.get("status")
                    )
                ),

                minutes_to_hhmm(
                    r.get("overtime_minutes", 0)
                ),

                minutes_to_hhmm(
                    r.get("early_leave_minutes", 0)
                ),

                minutes_to_hhmm(
                    r.get("late_minutes", 0)
                ),

                minutes_to_hhmm(
                    r.get("worked_minutes", 0)
                ),

                fmt_time(
                    r.get("last_punch")
                ),

                fmt_time(
                    r.get("first_punch")
                ),

                fmt_date(
                    r.get("date")
                ),

                ar(day_ar),
            ])

        attendance_table = Table(
            table_data,
            colWidths=[
                70,
                55,
                72,
                55,
                62,
                55,
                55,
                70,
                55
            ],
            repeatRows=1
        )

        attendance_table.setStyle(
            TableStyle([

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Arabic"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    8.5
                ),

                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    8
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#dbeafe")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.black
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
            ])
        )

        elements.append(
            attendance_table
        )

    # =====================================================
    # LEAVES SECTION
    # =====================================================

    elements.append(
        Spacer(1, 16)
    )

    elements.append(
        Paragraph(
            ar("الإجازات المعتمدة"),
            section_style
        )
    )

    leave_df = data_df[
        data_df["status"]
        .astype(str)
        .str.contains("إجازة")
    ]

    if leave_df.empty:

        elements.append(
            Paragraph(
                ar("لا توجد إجازات"),
                normal_style
            )
        )

    else:

        leave_table = [[

            ar("نوع الإجازة"),

            ar("الحالة"),

            ar("التاريخ"),

            ar("اليوم"),
        ]]

        for _, r in leave_df.iterrows():

            day_en = safe_str(
                r.get("weekday")
            )

            day_ar = (
                safe_str(
                    r.get("weekday_ar")
                )
                or WEEKDAY_AR.get(
                    day_en,
                    day_en
                )
            )

            leave_table.append([

                ar(
                    safe_str(
                        r.get("leave_type")
                    )
                ),

                ar(
                    safe_str(
                        r.get("status")
                    )
                ),

                fmt_date(
                    r.get("date")
                ),

                ar(day_ar),
            ])

        leaves_table = Table(
            leave_table,
            colWidths=[
                120,
                120,
                100,
                80
            ],
            repeatRows=1
        )

        leaves_table.setStyle(
            TableStyle([

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Arabic"
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#dcfce7")
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
            ])
        )

        elements.append(
            leaves_table
        )

    # =====================================================
    # TOTALS
    # =====================================================

    elements.append(
        Spacer(1, 12)
    )

    calc_df = data_df[

        ~data_df["status"]
        .astype(str)
        .str.contains("إجازة")
    ]

    total_late = int(
        calc_df["late_minutes"].sum()
    ) if "late_minutes" in calc_df.columns else 0

    total_early = int(
        calc_df["early_leave_minutes"].sum()
    ) if "early_leave_minutes" in calc_df.columns else 0

    total_overtime = int(
        calc_df["overtime_minutes"].sum()
    ) if "overtime_minutes" in calc_df.columns else 0

    elements.append(
        Paragraph(
            ar(
                f"إجمالي التأخير: "
                f"{minutes_to_ar_text(total_late)}"
            ),
            total_style
        )
    )

    elements.append(
        Paragraph(
            ar(
                f"إجمالي الخروج المبكر: "
                f"{minutes_to_ar_text(total_early)}"
            ),
            total_style
        )
    )

    elements.append(
        Paragraph(
            ar(
                f"إجمالي الإضافي: "
                f"{minutes_to_ar_text(total_overtime)}"
            ),
            total_style
        )
    )

    # =====================================================
    # BUILD
    # =====================================================

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
