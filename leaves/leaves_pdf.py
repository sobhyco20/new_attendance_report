from io import BytesIO
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

import arabic_reshaper

from bidi.algorithm import get_display

from leaves.leaves_helpers import (
    safe_str,
    fmt_date
)

# =========================================================
# FONT
# =========================================================

pdfmetrics.registerFont(
    TTFont(
        "Arabic",
        "fonts/Cairo-Regular.ttf"
    )
)

pdfmetrics.registerFont(
    TTFont(
        "ArabicBold",
        "fonts/Cairo-Bold.ttf"
    )
)

# =========================================================
# RTL TEXT
# =========================================================

def rtl(text):

    text = safe_str(text)

    reshaped = arabic_reshaper.reshape(text)

    return get_display(reshaped)

# =========================================================
# PDF
# =========================================================

def build_leaves_pdf(df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(

        buffer,

        pagesize=landscape(A4),

        rightMargin=15,
        leftMargin=15,

        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # RTL STYLE
    # =====================================================

    rtl_style = ParagraphStyle(

        "rtl",

        parent=styles["Normal"],

        fontName="Arabic",

        fontSize=10,

        leading=14,

        alignment=TA_RIGHT,
    )

    title_style = ParagraphStyle(

        "title",

        parent=styles["Title"],

        fontName="ArabicBold",

        fontSize=22,

        leading=28,

        alignment=TA_RIGHT,

        textColor=colors.HexColor("#1d4ed8")
    )

    elements = []

    # =====================================================
    # TITLE
    # =====================================================

    title = Paragraph(

        rtl("تقرير الإجازات"),

        title_style
    )

    elements.append(title)

    elements.append(
        Spacer(1, 18)
    )

    # =====================================================
    # EMPTY
    # =====================================================

    if df is None or df.empty:

        empty = Paragraph(

            rtl("لا توجد بيانات إجازات"),

            rtl_style
        )

        elements.append(empty)

        doc.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf

    # =====================================================
    # TABLE HEADER
    # =====================================================

    data = [[

        rtl("ملاحظات"),

        rtl("المرفق"),

        rtl("الحالة"),

        rtl("إلى"),

        rtl("من"),

        rtl("نوع الإجازة"),

        rtl("القسم"),

        rtl("الرقم الوظيفي"),

        rtl("اسم الموظف"),
    ]]
    # =====================================================
    # ROWS
    # =====================================================

    for _, r in df.iterrows():

        attachment = safe_str(
            r.get("attachment_name")
        )

        if attachment:
            attachment = "يوجد مرفق"

        else:
            attachment = "-"

        row = [

            Paragraph(
                rtl(
                    r.get("notes")
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    attachment
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    r.get("status")
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    fmt_date(
                        r.get("end_date")
                    )
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    fmt_date(
                        r.get("start_date")
                    )
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    r.get("leave_type")
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    r.get("department")
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    r.get("employee_no")
                ),
                rtl_style
            ),

            Paragraph(
                rtl(
                    r.get("name_ar")
                ),
                rtl_style
            ),
        ]

        data.append(row)

    # =====================================================
    # WIDTHS
    # =====================================================

    col_widths = [

        110,  # notes
        60,   # attachment
        60,   # status
        70,   # end
        70,   # start
        75,   # leave type
        120,   # department
        70,   # emp no
        120,  # employee
    ]

    # =====================================================
    # TABLE
    # =====================================================

    table = Table(

        data,

        colWidths=col_widths,

        repeatRows=1
    )

    # =====================================================
    # STYLE
    # =====================================================

    table.setStyle(TableStyle([

        # HEADER
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1d4ed8")
        ),

        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),

        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "ArabicBold"
        ),

        (
            "FONTSIZE",
            (0, 0),
            (-1, 0),
            11
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, 0),
            12
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, 0),
            12
        ),

        # BODY
        (
            "FONTNAME",
            (0, 1),
            (-1, -1),
            "Arabic"
        ),

        (
            "FONTSIZE",
            (0, 1),
            (-1, -1),
            9
        ),

        (
            "BACKGROUND",
            (0, 1),
            (-1, -1),
            colors.whitesmoke
        ),

        (
            "TEXTCOLOR",
            (0, 1),
            (-1, -1),
            colors.black
        ),

        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.HexColor("#d1d5db")
        ),

        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "RIGHT"
        ),

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),

        (
            "BOTTOMPADDING",
            (0, 1),
            (-1, -1),
            8
        ),

        (
            "TOPPADDING",
            (0, 1),
            (-1, -1),
            8
        ),

        # ROW COLORS
        (
            "ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [
                colors.white,
                colors.HexColor("#f8fafc")
            ]
        ),
    ]))

    elements.append(table)

    # =====================================================
    # BUILD
    # =====================================================

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf