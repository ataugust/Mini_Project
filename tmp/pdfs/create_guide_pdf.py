import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


SOURCE = Path(r"C:\Users\USER\.codex\attachments\66c50ec9-02d0-4896-86ba-4c2a239f1dbe\pasted-text.txt")
OUTPUT = Path(r"D:\Mini_project\output\pdf\guide explanation.pdf")

NAVY = colors.HexColor("#172934")
TEAL = colors.HexColor("#3E8091")
PALE_TEAL = colors.HexColor("#EAF3F5")
INK = colors.HexColor("#263640")
MUTED = colors.HexColor("#60717B")
LINE = colors.HexColor("#D8E2E6")
LIGHT = colors.HexColor("#F5F8F9")
WHITE = colors.white


def normalize_text(value: str) -> str:
    replacements = {
        "â€”": "-", "â€“": "-", "âˆ’": "-", "â†’": "->", "â†“": "v",
        "Ã—": "x", "â‰ˆ": "approximately", "âˆž": "infinity", "Â·": "*",
        "â€™": "'", "â€œ": '"', "â€": '"', "â€˜": "'", "â€¦": "...",
        "Î±": "alpha", "Î²": "beta", "Î”": "delta", "Ï„": "tau",
        "Î¸": "theta", "Î»": "lambda", "â‚˜": "_m", "â‚‚": "_2",
        "â”œâ”€â”€": "|-", "â””â”€â”€": "`-", "â”€": "-",
    }
    for broken, repaired in replacements.items():
        value = value.replace(broken, repaired)
    unicode_replacements = {
        "—": "-", "–": "-", "−": "-", "→": "->", "↓": "v",
        "×": "x", "·": "*", "≈": "approximately", "∞": "infinity",
        "₂": "2", "ₘ": "_m", "├──": "|-", "└──": "`-", "─": "-",
    }
    for original, repaired in unicode_replacements.items():
        value = value.replace(original, repaired)
    value = value.replace("[`", "[").replace("()`]", "()]" )
    value = re.sub(r"\[([^\]]+)\]\((?:D:/Mini_project/Impementation/agent-memory/)?([^\)]+)\)", r"\1 - \2", value)
    value = value.replace("<id>", "memory-id")
    return value


class GuideDocument(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="main",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="guide", frames=[frame], onPage=self.draw_page))

    def draw_page(self, canvas, doc):
        page = canvas.getPageNumber()
        if page == 1:
            canvas.setFillColor(NAVY)
            canvas.rect(0, A4[1] - 102 * mm, A4[0], 102 * mm, fill=1, stroke=0)
            canvas.setFillColor(TEAL)
            canvas.rect(0, A4[1] - 105 * mm, A4[0], 3 * mm, fill=1, stroke=0)
            return
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(self.leftMargin, A4[1] - 18 * mm, A4[0] - self.rightMargin, A4[1] - 18 * mm)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, A4[1] - 14 * mm, "UAMR - GUIDE EXPLANATION")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(A4[0] - self.rightMargin, 13 * mm, f"Page {page - 1}")
        canvas.setFillColor(TEAL)
        canvas.circle(self.leftMargin, 13 * mm, 1.3 * mm, fill=1, stroke=0)
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in {"Section", "Subsection"}:
            level = 0 if flowable.style.name == "Section" else 1
            text = flowable.getPlainText()
            key = f"heading-{level}-{self.seq.nextf('heading')}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9, leading=12, textColor=colors.HexColor("#9ECBD5"),
    spaceAfter=9, uppercase=True,
))
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=27, leading=32, textColor=WHITE, alignment=TA_LEFT, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="CoverSubtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=12, leading=18, textColor=colors.HexColor("#D7E7EB"), spaceAfter=16,
))
styles.add(ParagraphStyle(
    name="CoverMeta", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9, leading=14, textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=17, leading=22, textColor=NAVY, spaceBefore=12, spaceAfter=8,
    keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11.5, leading=15, textColor=TEAL, spaceBefore=9, spaceAfter=5,
    keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="BodyGuide", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.4, leading=14.2, textColor=INK, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="BulletGuide", parent=styles["BodyGuide"], leftIndent=4, firstLineIndent=0,
    spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="CodeGuide", parent=styles["Code"], fontName="Courier",
    fontSize=8.3, leading=12, textColor=NAVY, backColor=LIGHT,
    borderColor=LINE, borderWidth=0.5, borderPadding=7, spaceBefore=3,
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyGuide"], fontName="Helvetica-Bold",
    fontSize=10, leading=15, leftIndent=12, rightIndent=12, textColor=NAVY,
    backColor=PALE_TEAL, borderColor=TEAL, borderWidth=0.7,
    borderPadding=10, spaceBefore=5, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="TOCHeading", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=22, textColor=NAVY, spaceAfter=15,
))
styles.add(ParagraphStyle(
    name="SmallNote", parent=styles["BodyGuide"], fontSize=8.2,
    leading=12, textColor=MUTED,
))


SECTION_HEADINGS = {
    "1. Project title", "2. Short explanation for your guide", "3. Why this project is needed",
    "4. System architecture", "5. How one chat request works", "6. Research instrumentation",
    "7. The four UAMR signals", "7.1 Retrieval frequency - F(m)", "7.2 Recency - R(m)",
    "7.3 Retrieval quality - Q(m)", "7.4 Redundancy - D(m)", "8. Final retention equation",
    "9. How we developed our own equation", "10. Cold-start grace period",
    "11. Memory-budget algorithm", "12. ACTIVE and PRUNED do not mean deletion",
    "13. Deterministic explanations", "14. PCA vector memory map", "15. Why PCA is cached",
    "16. Memory Lab explanation", "17. Policy Engine explanation",
    "18. Important backend classes and functions", "19. What is original in the project?",
    "20. Current limitations", "21. Future experimental work",
    "22. Suggested final presentation statement",
}

SUBHEADINGS = {
    "Responsibilities", "Ollama and Qwen3", "Mem0", "ChromaDB", "SQLite research database", "UAMR",
    "Why instrumentation was required", "Retrieval event", "Aggregate usage data",
    "Name of the mathematical technique", "Why smoothing is needed", "Interpretation", "Function used",
    "Name of the equation", "Why we used exponential decay", "Meaning of tau", "Never-retrieved memories",
    "Name of the technique", "Why rank is important", "Why similarity alone is insufficient", "Functions used",
    "Name of the similarity equation", "Redundancy threshold", "Name of this transformation", "Example",
    "Why compare only against higher-value memories?", "Why three positive terms and one negative term?",
    "Real calculation example", "The equation-design process", "Step 1: Define the objective",
    "Step 2: Identify observable evidence", "Step 3: Keep signals on comparable scales",
    "Step 4: Combine positive evidence", "Step 5: Add a duplication penalty",
    "Step 6: Separate scoring from the budget decision", "Step 7: Add cold-start protection",
    "Step 8: Make everything configurable", "Mean centering", "Singular Value Decomposition",
    "Projection", "Why PCA?", "Important limitation", "Memory table", "Detail drawer",
    "Budget simulator",
}


def paragraph(text: str, style="BodyGuide"):
    return Paragraph(html.escape(text), styles[style])


def is_code_like(line: str) -> bool:
    stripped = line.strip()
    if len(stripped) > 115:
        return False
    code_markers = (" = ", "()", "_count", "_sum", "_at", "_id", "[0.", "ceil(", "cosine(", "numpy.")
    return any(marker in stripped for marker in code_markers) or stripped in {
        "B < N", "ACTIVE / PRUNED", "F", "R", "Q", "D", "S",
        "event_id", "memory_id", "interaction_number", "query", "similarity_score",
        "retrieval_rank", "timestamp", "retrieval_count", "created_interaction",
        "created_at", "last_retrieved_interaction", "last_retrieved_at",
        "similarity_sum", "rank_discounted_relevance_sum", "average_similarity",
        "average_retrieval_rank", "frequency_score", "recency_score",
        "retrieval_quality_score", "redundancy_score", "retention_score", "state",
    }


def build_story(text: str):
    lines = [normalize_text(line).strip() for line in text.splitlines()]
    story = []

    # Cover
    story.extend([
        Spacer(1, 24 * mm),
        Paragraph("FINAL-YEAR PROJECT RESEARCH GUIDE", styles["CoverKicker"]),
        Paragraph("Usage-Aware Memory Retention<br/>for Long-Term AI Agents", styles["CoverTitle"]),
        Paragraph("A guide-ready explanation of the architecture, equations, implementation, originality, limitations, and demonstration workflow.", styles["CoverSubtitle"]),
        Spacer(1, 55 * mm),
        Paragraph("UAMR Research Project", ParagraphStyle(name="MetaTitle", parent=styles["CoverMeta"], fontName="Helvetica-Bold", fontSize=12, textColor=NAVY, spaceAfter=5)),
        Paragraph("FastAPI  |  Ollama  |  Qwen3  |  Mem0  |  ChromaDB  |  SQLite  |  React", styles["CoverMeta"]),
        Spacer(1, 7 * mm),
        Paragraph("Prepared as a complete technical explanation for project-guide discussion and final-year demonstration.", styles["CoverMeta"]),
        PageBreak(),
    ])

    # Contents
    story.append(Paragraph("Contents", styles["TOCHeading"]))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name="TOC1", fontName="Helvetica-Bold", fontSize=9, leading=13, leftIndent=0, firstLineIndent=0, textColor=NAVY, spaceBefore=3),
        ParagraphStyle(name="TOC2", fontName="Helvetica", fontSize=8, leading=11, leftIndent=12, firstLineIndent=0, textColor=MUTED),
    ]
    story.append(toc)
    story.append(PageBreak())

    # Skip the pasted document title; the designed cover replaces it.
    start = 1 if lines and lines[0].startswith("Guide-ready explanation") else 0
    bullet_buffer = []
    table_rows = []
    in_function_table = False

    def flush_bullets():
        nonlocal bullet_buffer
        if bullet_buffer:
            story.append(ListFlowable(
                [ListItem(paragraph(item, "BulletGuide"), leftIndent=8) for item in bullet_buffer],
                bulletType="bullet", start="circle", leftIndent=16, bulletFontName="Helvetica",
                bulletFontSize=6, bulletColor=TEAL, spaceAfter=6,
            ))
            bullet_buffer = []

    def flush_table():
        nonlocal table_rows, in_function_table
        if table_rows:
            table = Table(table_rows, colWidths=[42 * mm, 45 * mm, 78 * mm], repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("LEADING", (0, 0), (-1, -1), 10.5),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(table)
            story.append(Spacer(1, 6))
            table_rows = []
        in_function_table = False

    callout_next = False
    for line in lines[start:]:
        if not line:
            flush_bullets()
            if in_function_table:
                flush_table()
            continue
        if line in SECTION_HEADINGS:
            flush_bullets()
            flush_table()
            story.append(Paragraph(html.escape(line), styles["Section"]))
            callout_next = line in {"2. Short explanation for your guide", "19. What is original in the project?", "22. Suggested final presentation statement"}
            continue
        if line == "Component\tFunction\tPurpose":
            flush_bullets()
            in_function_table = True
            table_rows = [[paragraph(cell, "SmallNote") for cell in line.split("\t")]]
            continue
        if in_function_table and "\t" in line:
            table_rows.append([paragraph(cell, "SmallNote") for cell in line.split("\t")])
            continue
        if line in SUBHEADINGS:
            flush_bullets()
            story.append(Paragraph(html.escape(line), styles["Subsection"]))
            continue
        if line.startswith("- "):
            bullet_buffer.append(line[2:])
            continue
        flush_bullets()
        if callout_next and line not in {"You can begin with this:", "A good academic answer is:"}:
            story.append(paragraph(line, "Callout"))
            callout_next = False
        elif line in {"You can begin with this:", "The main research question is:", "Our contribution is:", "A good academic answer is:", "Instead say:"}:
            story.append(Paragraph(html.escape(line), styles["Subsection"]))
            callout_next = True
        elif is_code_like(line):
            story.append(paragraph(line, "CodeGuide"))
        elif len(line) < 48 and line.endswith(":"):
            story.append(Paragraph(html.escape(line), styles["Subsection"]))
        else:
            story.append(paragraph(line))

    flush_bullets()
    flush_table()
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    text = SOURCE.read_text(encoding="utf-8")
    document = GuideDocument(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=24 * mm,
        bottomMargin=21 * mm,
        title="Guide Explanation - Usage-Aware Memory Retention",
        author="UAMR Research Project",
        subject="Guide-ready technical explanation of the UAMR final-year project",
    )
    document.multiBuild(build_story(text))
    print(OUTPUT)


if __name__ == "__main__":
    main()
