from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

from reportlab.platypus.flowables import HRFlowable

from reportlab.lib import colors

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

from reportlab.lib.styles import ParagraphStyle

import re
import os


# ---------------------------------------------------
# CLEAN LATEX FOR PDF DISPLAY
# ---------------------------------------------------

def clean_latex(text):

    # Remove $$ blocks
    text = text.replace("$$", "")

    # Remove inline $
    text = text.replace("$", "")

    # Convert common LaTeX symbols

    replacements = {

        r"\\Delta": "Δ",
        r"\\theta": "θ",
        r"\\alpha": "α",
        r"\\beta": "β",
        r"\\gamma": "γ",
        r"\\mu": "μ",
        r"\\pi": "π",
        r"\\times": "×",
        r"\\cdot": "·",
        r"\\degree": "°",
        r"\\circ": "°",
        r"\\rightarrow": "→",

        r"\\frac": "/",

        r"\\text": "",

        "{": "",
        "}": "",

        "\\\\": "",
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    return text


# ---------------------------------------------------
# GENERATE PDF
# ---------------------------------------------------

def generate_pdf(subject, chapter, topic, content):

    # ---------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------------

    os.makedirs("outputs/pdfs", exist_ok=True)

    # ---------------------------------------------------
    # UNIQUE PDF NAME
    # ---------------------------------------------------

    safe_topic = topic.replace(" ", "_")

    pdf_path = f"outputs/pdfs/{safe_topic}.pdf"

    # ---------------------------------------------------
    # PDF DOCUMENT
    # ---------------------------------------------------

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=28,
    )

    styles = getSampleStyleSheet()

    # ---------------------------------------------------
    # CUSTOM STYLES
    # ---------------------------------------------------

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=18,
        leading=24,
        textColor=colors.darkred,
        spaceBefore=14,
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontSize=12,
        leading=22,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
    )

    formula_style = ParagraphStyle(
        "FormulaStyle",
        parent=styles["BodyText"],
        fontSize=13,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceBefore=8,
        spaceAfter=8,
    )

    # ---------------------------------------------------
    # PDF ELEMENTS
    # ---------------------------------------------------

    elements = []

    # ---------------------------------------------------
    # TITLE PAGE
    # ---------------------------------------------------

    elements.append(
        Paragraph("ChemEduAI Study Material", title_style)
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(f"<b>Subject:</b> {subject}", normal_style)
    )

    elements.append(
        Paragraph(f"<b>Chapter:</b> {chapter}", normal_style)
    )

    elements.append(
        Paragraph(f"<b>Topic:</b> {topic}", normal_style)
    )

    elements.append(Spacer(1, 20))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=colors.grey,
        )
    )

    elements.append(Spacer(1, 25))

    # ---------------------------------------------------
    # CONTENT PROCESSING
    # ---------------------------------------------------

    lines = content.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # -----------------------------------------------
        # HEADINGS
        # -----------------------------------------------

        if line.startswith("# "):

            text = line.replace("# ", "")

            elements.append(
                Paragraph(text, heading_style)
            )

            continue

        elif line.startswith("## "):

            text = line.replace("## ", "")

            elements.append(
                Paragraph(text, heading_style)
            )

            continue

        elif line.startswith("### "):

            text = line.replace("### ", "")

            elements.append(
                Paragraph(text, heading_style)
            )

            continue

        # -----------------------------------------------
        # FORMULAS
        # -----------------------------------------------

        elif (
            "\\" in line
            or "=" in line
            or "^" in line
            or "frac" in line
        ):

            formula_text = clean_latex(line)

            elements.append(
                Paragraph(formula_text, formula_style)
            )

            continue

        # -----------------------------------------------
        # NORMAL TEXT
        # -----------------------------------------------

        else:

            clean_text = clean_latex(line)

            elements.append(
                Paragraph(clean_text, normal_style)
            )

    # ---------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------

    doc.build(elements)

    # ---------------------------------------------------
    # RETURN PDF PATH
    # ---------------------------------------------------

    return pdf_path