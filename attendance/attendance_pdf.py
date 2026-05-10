from io import BytesIO
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


pdfmetrics.registerFont(
    TTFont("Arabic", "fonts/Amiri-Regular.ttf")
)

pdfmetrics.registerFont(
    TTFont("ArabicBold", "fonts/Amiri-Bold.ttf")
)


WEEKDAY_AR = {
    "Saturday": "السبت",
    "Sunday": "الأحد",
    "Monday": "الإثنين",
    "Tuesday": "الثلاثاء",
    "Wednesday": "الأربعاء",
    "Thursday": "الخميس",
    "Friday": "الجمعة",
}


def ar(text):
    if text is None:
        return ""

    text = str(text)
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


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
        return pd.to_datetime(v).strftime("%d-%m-%Y")
    except Exception:
        return ""


def fmt_time(v):
    try:
        if pd.isna(v):
            return ""
        return pd.to_datetime(v).strftime("%H:%M")
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
        d = pd.to_datetime(df["date"].dropna().max())
        return f"تقرير الموظف عن شهر {d.month:02d} - {d.year}"
    except Exception:
        return "تقرير الموظف"


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

    title_style = ParagraphStyle(
        "title",
        parent=styles["Normal"],
        fontName="ArabicBold",
        fontSize=16,
        alignment=1,
        leading=22,
    )

    name_style = ParagraphStyle(
        "name",
        parent=styles["Normal"],
        fontName="ArabicBold",
        fontSize=12,
        alignment=1,
        leading=18,
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
        fontSize=11,
        alignment=2,
        leading=16,
        spaceBefore=8,
        spaceAfter=6,
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
        leading=15,
    )

    elements = []

    if df is None or df.empty:
        elements.append(Paragraph(ar("لا توجد بيانات"), title_style))
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    data_df = df.copy()
    data_df["date"] = pd.to_datetime(data_df["date"], errors="coerce")
    data_df = data_df.sort_values("date")

    first = data_df.iloc[0]

    employee_name = safe_str(first.get("employee_name", ""))
    employee_id = safe_str(first.get("employee_id", ""))
    department = safe_str(first.get("department", ""))
    job_title = safe_str(first.get("job_title", ""))
    nationality = safe_str(first.get("nationality", ""))

    title = month_title(data_df)

    elements.append(Paragraph(ar(title), title_style))
    elements.append(Paragraph(ar(employee_name), name_style))

    info_parts = []

    if employee_id:
        info_parts.append(f"الكود/الرقم: {employee_id}")

    if job_title:
        info_parts.append(f"الوظيفة: {job_title}")

    if department:
        info_parts.append(f"الإدارة: {department}")

    if nationality:
        info_parts.append(f"الجنسية: {nationality}")

    if info_parts:
        elements.append(
            Paragraph(
                ar(" | ".join(info_parts)),
                info_style
            )
        )

    elements.append(Spacer(1, 8))

    note = "ملاحظة: يتم احتساب التأخير بعد بداية الدوام مع السماح، والخروج المبكر قبل نهاية الدوام، والإضافي بعد نهاية الدوام."
    elements.append(Paragraph(ar(note), normal_style))
    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(
            ar("التأخير والخروج المبكر والإضافي"),
            section_style
        )
    )

    table_data = [[
        ar("الإضافي"),
        ar("الخروج المبكر"),
        ar("التأخير"),
        ar("ساعات العمل"),
        ar("آخر بصمة"),
        ar("أول بصمة"),
        ar("التاريخ"),
        ar("اليوم"),
    ]]

    for _, r in data_df.iterrows():

        day_en = safe_str(r.get("weekday", ""))
        day_ar = safe_str(r.get("weekday_ar", "")) or WEEKDAY_AR.get(day_en, day_en)

        table_data.append([

            minutes_to_hhmm(
                r.get("overtime_minutes", 0)
            ),

            minutes_to_hhmm(
                r.get("early_leave_minutes", 0)
            ),

            minutes_to_hhmm(
                r.get("late_minutes", 0)
            ),

            safe_str(
                r.get(
                    "work_hours",
                    minutes_to_hhmm(
                        r.get("worked_minutes", 0)
                    )
                )
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
        colWidths=[55, 72, 55, 62, 55, 55, 70, 55],
        repeatRows=1
    )

    attendance_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Arabic"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(attendance_table)
    elements.append(Spacer(1, 10))

    total_late = int(data_df["late_minutes"].sum()) if "late_minutes" in data_df.columns else 0
    total_early = int(data_df["early_leave_minutes"].sum()) if "early_leave_minutes" in data_df.columns else 0
    total_overtime = int(data_df["overtime_minutes"].sum()) if "overtime_minutes" in data_df.columns else 0

    net_minutes = total_overtime - (total_late + total_early)

    elements.append(
        Paragraph(
            ar(f"إجمالي التأخير: {minutes_to_ar_text(total_late)}"),
            total_style
        )
    )

    elements.append(
        Paragraph(
            ar(f"إجمالي الخروج المبكر: {minutes_to_ar_text(total_early)}"),
            total_style
        )
    )

    elements.append(
        Paragraph(
            ar(f"إجمالي الإضافي: {minutes_to_ar_text(total_overtime)}"),
            total_style
        )
    )

    if net_minutes > 0:
        net_text = f"الصافي النهائي: إضافي {minutes_to_ar_text(net_minutes)}"
    elif net_minutes < 0:
        net_text = f"الصافي النهائي: تأخير {minutes_to_ar_text(net_minutes)}"
    else:
        net_text = "الصافي النهائي: متعادل 0 ساعة و 0 دقيقة"

    elements.append(
        Paragraph(
            ar(net_text),
            total_style
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            ar("الغياب"),
            section_style
        )
    )

    absence_df = data_df[data_df.get("status", "") == "غائب"].copy()

    if absence_df.empty:
        elements.append(
            Paragraph(
                ar("لا يوجد غياب"),
                normal_style
            )
        )
    else:
        absence_data = [[
            ar("اليوم"),
            ar("التاريخ")
        ]]

        for _, r in absence_df.iterrows():

            day_en = safe_str(r.get("weekday", ""))
            day_ar = safe_str(r.get("weekday_ar", "")) or WEEKDAY_AR.get(day_en, day_en)

            absence_data.append([
                ar(day_ar),
                fmt_date(r.get("date"))
            ])

        absence_table = Table(
            absence_data,
            colWidths=[120, 120],
            repeatRows=1
        )

        absence_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Arabic"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        elements.append(absence_table)
        elements.append(Spacer(1, 6))
        elements.append(
            Paragraph(
                ar(f"عدد أيام الغياب: {len(absence_df)}"),
                total_style
            )
        )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            ar("الإجازات المعتمدة"),
            section_style
        )
    )

    leave_df = data_df[data_df.get("status", "") == "إجازة"].copy()

    if leave_df.empty:
        elements.append(
            Paragraph(
                ar("لا توجد إجازات معتمدة"),
                normal_style
            )
        )
    else:
        leave_data = [[
            ar("اليوم"),
            ar("التاريخ"),
            ar("نوع الإجازة")
        ]]

        for _, r in leave_df.iterrows():

            day_en = safe_str(r.get("weekday", ""))
            day_ar = safe_str(r.get("weekday_ar", "")) or WEEKDAY_AR.get(day_en, day_en)

            leave_data.append([
                ar(day_ar),
                fmt_date(r.get("date")),
                ar(safe_str(r.get("leave_type", "إجازة")))
            ])

        leave_table = Table(
            leave_data,
            colWidths=[110, 110, 160],
            repeatRows=1
        )

        leave_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Arabic"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        elements.append(leave_table)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf