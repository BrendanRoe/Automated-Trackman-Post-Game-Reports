from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)

from charts import PITCH_COLORS

# --------------------------------------------------
# NC STATE COLOR PALETTE
# --------------------------------------------------

NCSTATE_RED = colors.HexColor("#CC0000")
NCSTATE_BLACK = colors.HexColor("#000000")
NCSTATE_WHITE = colors.HexColor("#FFFFFF")

LIGHT_GRAY = colors.HexColor("#F2F2F2")
MEDIUM_GRAY = colors.HexColor("#CCCCCC")
DARK_GRAY = colors.HexColor("#666666")


def create_pitcher_pdf(
    report,
    output_path,
    pitch_location_chart=None,
    pitch_usage_chart=None,
    pitch_movement_chart=None,
    opponent=None,
    game_date=None
):
    pitcher = report["pitcher"]
    total_pitches = report["total_pitches"]
    overall = report["overall"]
    pitch_metrics = report["pitch_metrics"]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], alignment=TA_CENTER,
        fontSize=20, leading=24, spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle", parent=styles["Normal"], alignment=TA_CENTER,
        fontSize=10, leading=12, spaceAfter=18
    )
    section_style = ParagraphStyle(
    "SectionHeader",
    parent=styles["Heading2"],
    fontSize=11,
    leading=14,
    textColor=NCSTATE_WHITE,
    spaceBefore=6,
    spaceAfter=3,
    leftIndent=6,
)

    page2_section_style = ParagraphStyle(
        "Page2SectionHeader",
        parent=section_style,
        spaceBefore=2,
        spaceAfter=2,
    )

    normal_style = ParagraphStyle(
        "NormalReport", parent=styles["Normal"], fontSize=9, leading=12
    )
    pitch_usage_section_style = ParagraphStyle(
        "PitchUsageHeader",
        parent=section_style,
        spaceBefore=1,
        spaceAfter=1,
    )

    story = []

    def add_section_header(title):
        section_table = Table(
        [[Paragraph(title, section_style)]],
        colWidths=[7.0 * inch],
    )

        section_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    NCSTATE_BLACK,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    NCSTATE_WHITE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
            ]
        )
    )

        story.append(section_table)

    # --------------------------------------------------
    # NC STATE HEADER
    # --------------------------------------------------

    header_table = Table(
        [
            [
                Paragraph(
                    pitcher.upper(),
                    ParagraphStyle(
                        "HeaderPitcher",
                        parent=title_style,
                        textColor=NCSTATE_WHITE,
                        fontSize=20,
                        leading=23,
                        alignment=TA_CENTER,
                    ),
                )
            ],
            [
                Paragraph(
                    f"POST-GAME PITCHING REPORT — vs. {opponent} | {game_date}",
                    ParagraphStyle(
                        "HeaderSubtitle",
                        parent=subtitle_style,
                        textColor=NCSTATE_WHITE,
                        fontSize=9,
                        leading=11,
                        alignment=TA_CENTER,
                    ),
                )
            ],
        ],
        colWidths=[7.0 * inch],
    )

    header_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    NCSTATE_BLACK,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(header_table)

    accent_line = Table(
        [[""]],
        colWidths=[7.0 * inch],
        rowHeights=[0.08 * inch],
    )

    accent_line.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    NCSTATE_RED,
                ),
            ]
        )
    )

    story.append(accent_line)
    story.append(Spacer(1, 0.01 * inch))

    story.append(Paragraph("OVERALL METRICS", section_style))

    overall_data = [
        ["Total Pitches", "Strike %", "Whiff %", "CSW %", "Chase %"],
        [
            str(total_pitches),
            f"{overall['strike_pct']:.1f}%",
            f"{overall['whiff_pct']:.1f}%",
            f"{overall['csw_pct']:.1f}%",
            f"{overall['chase_pct']:.1f}%",
        ],
    ]

    overall_table = Table(
        overall_data,
        colWidths=[1.25 * inch] * 5,
    )
    overall_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    NCSTATE_BLACK,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    NCSTATE_WHITE,
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, 1),
                    NCSTATE_RED,
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, 1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    8,
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, 1),
                    12,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    MEDIUM_GRAY,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    NCSTATE_BLACK,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )
    story.append(overall_table)

    story.append(Paragraph("PITCH ARSENAL", section_style))

    arsenal_data = [[
        "Pitch", "Usage", "Avg Velo", "Max Velo",
        "Spin", "IVB", "HB", "Ext.", "Rel Ht.", "VAA"
    ]]

    for pitch_type, metrics in pitch_metrics.items():
        arsenal_data.append([
            pitch_type,
                f"{metrics['usage_pct']:.1f}%",
                f"{metrics['avg_velocity']:.1f}",
                f"{metrics['max_velocity']:.1f}",
                f"{metrics['avg_spin']:.0f}",
                f"{metrics['avg_ivb']:.1f}",
                f"{metrics['avg_hb']:.1f}",
                f"{metrics['avg_extension']:.1f}",
                f"{metrics['avg_release_height']:.1f}",
                f"{metrics['avg_vaa']:.1f}",
        ])

    arsenal_table = Table(arsenal_data, repeatRows=1)
    arsenal_color_commands = []

    for row_index, pitch_type in enumerate(pitch_metrics.keys(), start=1):
        arsenal_color_commands.append(
    (
        "TEXTCOLOR",
        (0, row_index),
        (0, row_index),
        colors.HexColor(
            PITCH_COLORS.get(
                pitch_type,
                "#000000"
            )
        ),
    )
)
    arsenal_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    NCSTATE_BLACK,
                ),
                *arsenal_color_commands,
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    NCSTATE_WHITE,
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    8,
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    MEDIUM_GRAY,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    NCSTATE_BLACK,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )
    story.append(arsenal_table)

    story.append(Paragraph("PITCH EFFECTIVENESS", section_style))

    effectiveness_data = [[
        "Pitch", "Strike %", "Whiff %", "CSW %", "Chase %"
    ]]

    for pitch_type, metrics in pitch_metrics.items():
        effectiveness_data.append([
            pitch_type,
            f"{metrics['strike_pct']:.1f}%",
            f"{metrics['whiff_pct']:.1f}%",
            f"{metrics['csw_pct']:.1f}%",
            f"{metrics['chase_pct']:.1f}%",
        ])

    effectiveness_table = Table(effectiveness_data, repeatRows=1)
    effectiveness_color_commands = []

    for row_index, pitch_type in enumerate(pitch_metrics.keys(), start=1):
        effectiveness_color_commands.append(
    (
        "TEXTCOLOR",
        (0, row_index),
        (0, row_index),
        colors.HexColor(
            PITCH_COLORS.get(
                pitch_type,
                "#000000"
            )
        ),
    )
)
    effectiveness_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    NCSTATE_BLACK,
                ),
                *effectiveness_color_commands,
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    NCSTATE_WHITE,
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    8,
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    MEDIUM_GRAY,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    NCSTATE_BLACK,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )
    story.append(effectiveness_table)
# --------------------------------------------------
# PITCH USAGE CHART
# --------------------------------------------------

    if pitch_usage_chart:

        story.append(
        Paragraph(
            "PITCH USAGE",
            pitch_usage_section_style
        )
    )

    pitch_usage_image = Image(
        pitch_usage_chart,
        width=7.0 * inch,
        height=2.8 * inch
    )

    story.append(
        pitch_usage_image
    )

    story.append(
        Spacer(1, 0 * inch)
    )


# --------------------------------------------------
# PITCH LOCATION CHART
# --------------------------------------------------

# --------------------------------------------------
# PITCH MOVEMENT + PITCH LOCATION
# --------------------------------------------------

    if pitch_location_chart:

        story.append(PageBreak())

    # --------------------------------------------------
    # NC STATE HEADER - PAGE 2
    # --------------------------------------------------

    story.append(header_table)
    story.append(accent_line)
    story.append(Spacer(1, 0.06 * inch))

# --------------------------------------------------
# PITCH MOVEMENT
# --------------------------------------------------

    story.append(
        Paragraph(
            "PITCH MOVEMENT",
            page2_section_style
        )
    )


    pitch_movement_image = Image(
        pitch_movement_chart,
        width=3.7 * inch,
        height=4.04 * inch,
    )

    pitch_movement_image.hAlign = "CENTER"

    story.append(pitch_movement_image)
    story.append(Spacer(1, 0 * inch))

    # --------------------------------------------------
    # PITCH LOCATION
    # --------------------------------------------------

    story.append(
        Paragraph(
            "PITCH LOCATION",
            page2_section_style
        )
    )



    pitch_location_image = Image(
        pitch_location_chart,
        width=3.7 * inch,
        height=4.04 * inch,
    )

    pitch_location_image.hAlign = "CENTER"

    story.append(pitch_location_image)
    story.append(Spacer(1, 0.15 * inch))


    # Build the PDF INSIDE the function.
    doc.build(story)
