"""
Digital Electrical Engineer (DEE)

SECTION 01 WORD REPORT GENERATOR

Generation of a Microsoft Word report for:

    SECTION 1
    SELECTION OF MAIN DIMENSIONS

Kopylov asynchronous motor design method.

Document formatting:

    Font: Times New Roman
    Font size: 14 pt
    Line spacing: 1.5
    First line indent: 1.25 cm
    Text alignment: justified

Equations are created as native Microsoft Word
Office Math objects using OMML.
"""

from pathlib import Path

from docx import Document

from docx.enum.text import (
    WD_ALIGN_PARAGRAPH,
)

from docx.enum.section import (
    WD_SECTION,
)

from docx.shared import (
    Pt,
    Cm,
)

from docx.oxml import OxmlElement

from docx.oxml.ns import (
    qn,
)


# ================================================================
# REPORT SETTINGS
# ================================================================

REPORT_DIRECTORY = Path(
    "reports"
)

REPORT_FILENAME = (
    "Section_01_Main_Dimensions.docx"
)

FONT_NAME = "Times New Roman"

FONT_SIZE_PT = 14

LINE_SPACING = 1.5

FIRST_LINE_INDENT_CM = 1.25


# ================================================================
# TEXT FORMATTING
# ================================================================

def set_run_font(
    run,
    font_name=FONT_NAME,
    font_size=FONT_SIZE_PT,
    bold=False,
    italic=False,
):
    """
    Apply font settings to a Word run.
    """

    run.font.name = font_name

    run.font.size = Pt(
        font_size
    )

    run.font.bold = bold

    run.font.italic = italic

    run_properties = run._element.get_or_add_rPr()

    run_fonts = run_properties.rFonts

    if run_fonts is None:

        run_fonts = OxmlElement(
            "w:rFonts"
        )

        run_properties.insert(
            0,
            run_fonts,
        )

    run_fonts.set(
        qn("w:ascii"),
        font_name,
    )

    run_fonts.set(
        qn("w:hAnsi"),
        font_name,
    )

    run_fonts.set(
        qn("w:eastAsia"),
        font_name,
    )

    run_fonts.set(
        qn("w:cs"),
        font_name,
    )


def format_paragraph(
    paragraph,
    alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    first_line_indent=True,
):
    """
    Apply standard report paragraph formatting.
    """

    paragraph.alignment = alignment

    paragraph_format = paragraph.paragraph_format

    paragraph_format.line_spacing = LINE_SPACING

    paragraph_format.space_before = Pt(
        0
    )

    paragraph_format.space_after = Pt(
        0
    )

    if first_line_indent:

        paragraph_format.first_line_indent = Cm(
            FIRST_LINE_INDENT_CM
        )

    else:

        paragraph_format.first_line_indent = Cm(
            0
        )


def add_text_paragraph(
    document,
    text,
    alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    first_line_indent=True,
):
    """
    Add a standard formatted text paragraph.
    """

    paragraph = document.add_paragraph()

    format_paragraph(
        paragraph=paragraph,
        alignment=alignment,
        first_line_indent=first_line_indent,
    )

    run = paragraph.add_run(
        text
    )

    set_run_font(
        run
    )

    return paragraph


def add_mixed_paragraph(
    document,
    parts,
    alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
    first_line_indent=True,
):
    """
    Add a paragraph containing differently formatted runs.

    parts format:

        [
            ("text", False, False),
            ("bold text", True, False),
            ("italic text", False, True),
        ]
    """

    paragraph = document.add_paragraph()

    format_paragraph(
        paragraph=paragraph,
        alignment=alignment,
        first_line_indent=first_line_indent,
    )

    for (
        text,
        bold,
        italic,
    ) in parts:

        run = paragraph.add_run(
            text
        )

        set_run_font(
            run=run,
            bold=bold,
            italic=italic,
        )

    return paragraph


# ================================================================
# SECTION TITLE
# ================================================================

def add_section_title(
    document,
    text,
):
    """
    Add section title.
    """

    paragraph = document.add_paragraph()

    format_paragraph(
        paragraph=paragraph,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        first_line_indent=False,
    )

    paragraph.paragraph_format.space_before = Pt(
        0
    )

    paragraph.paragraph_format.space_after = Pt(
        0
    )

    run = paragraph.add_run(
        text
    )

    set_run_font(
        run=run,
        bold=True,
    )

    return paragraph


# ================================================================
# OMML EQUATION ELEMENTS
# ================================================================

def create_math_run(
    text,
):
    """
    Create OMML mathematical run.
    """

    math_run = OxmlElement(
        "m:r"
    )

    math_run_properties = OxmlElement(
        "m:rPr"
    )

    math_style = OxmlElement(
        "m:sty"
    )

    math_style.set(
        qn("m:val"),
        "p",
    )

    math_run_properties.append(
        math_style
    )

    math_run.append(
        math_run_properties
    )

    math_text = OxmlElement(
        "m:t"
    )

    math_text.text = str(
        text
    )

    math_run.append(
        math_text
    )

    return math_run


def create_math_text(
    text,
):
    """
    Create a simple OMML math element.
    """

    return create_math_run(
        text
    )


def create_fraction(
    numerator,
    denominator,
):
    """
    Create OMML fraction.
    """

    fraction = OxmlElement(
        "m:f"
    )

    fraction_properties = OxmlElement(
        "m:fPr"
    )

    fraction.append(
        fraction_properties
    )

    numerator_element = OxmlElement(
        "m:num"
    )

    numerator_element.append(
        create_math_text(
            numerator
        )
    )

    denominator_element = OxmlElement(
        "m:den"
    )

    denominator_element.append(
        create_math_text(
            denominator
        )
    )

    fraction.append(
        numerator_element
    )

    fraction.append(
        denominator_element
    )

    return fraction


def create_superscript(
    base,
    exponent,
):
    """
    Create OMML superscript.
    """

    superscript = OxmlElement(
        "m:sSup"
    )

    superscript_properties = OxmlElement(
        "m:sSupPr"
    )

    superscript.append(
        superscript_properties
    )

    base_element = OxmlElement(
        "m:e"
    )

    base_element.append(
        create_math_text(
            base
        )
    )

    exponent_element = OxmlElement(
        "m:sup"
    )

    exponent_element.append(
        create_math_text(
            exponent
        )
    )

    superscript.append(
        base_element
    )

    superscript.append(
        exponent_element
    )

    return superscript


def create_radical(
    expression,
):
    """
    Create OMML square root.
    """

    radical = OxmlElement(
        "m:rad"
    )

    radical_properties = OxmlElement(
        "m:radPr"
    )

    hide_degree = OxmlElement(
        "m:degHide"
    )

    hide_degree.set(
        qn("m:val"),
        "1",
    )

    radical_properties.append(
        hide_degree
    )

    radical.append(
        radical_properties
    )

    degree_element = OxmlElement(
        "m:deg"
    )

    radical.append(
        degree_element
    )

    expression_element = OxmlElement(
        "m:e"
    )

    expression_element.append(
        create_math_text(
            expression
        )
    )

    radical.append(
        expression_element
    )

    return radical


# ================================================================
# EQUATION PARAGRAPH
# ================================================================

def add_equation(
    document,
    equation_elements,
    equation_number=None,
):
    """
    Add centered native Word equation.

    If equation_number is specified, a borderless
    3-column table is used:

        empty | equation | number

    This keeps the equation centered and the
    equation number aligned to the right.
    """

    if not isinstance(
        equation_elements,
        list,
    ):

        equation_elements = [
            equation_elements
        ]


    # ============================================================
    # EQUATION WITHOUT NUMBER
    # ============================================================

    if equation_number is None:

        paragraph = document.add_paragraph()

        format_paragraph(
            paragraph=paragraph,
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            first_line_indent=False,
        )

        math_paragraph = OxmlElement(
            "m:oMathPara"
        )

        math_object = OxmlElement(
            "m:oMath"
        )

        for element in equation_elements:

            math_object.append(
                element
            )

        math_paragraph.append(
            math_object
        )

        paragraph._element.append(
            math_paragraph
        )

        return paragraph


    # ============================================================
    # NUMBERED EQUATION
    # ============================================================

    table = document.add_table(
        rows=1,
        cols=3,
    )

    table.autofit = False

    table.columns[0].width = Cm(
        2.0
    )

    table.columns[1].width = Cm(
        12.0
    )

    table.columns[2].width = Cm(
        2.0
    )

    table_properties = table._tbl.tblPr

    table_borders = OxmlElement(
        "w:tblBorders"
    )

    for border_name in (
        "top",
        "left",
        "bottom",
        "right",
        "insideH",
        "insideV",
    ):

        border = OxmlElement(
            f"w:{border_name}"
        )

        border.set(
            qn("w:val"),
            "nil",
        )

        table_borders.append(
            border
        )

    table_properties.append(
        table_borders
    )


    # ============================================================
    # LEFT CELL
    # ============================================================

    left_cell = table.cell(
        0,
        0,
    )

    left_paragraph = left_cell.paragraphs[0]

    format_paragraph(
        paragraph=left_paragraph,
        alignment=WD_ALIGN_PARAGRAPH.LEFT,
        first_line_indent=False,
    )


    # ============================================================
    # EQUATION CELL
    # ============================================================

    equation_cell = table.cell(
        0,
        1,
    )

    equation_paragraph = equation_cell.paragraphs[0]

    format_paragraph(
        paragraph=equation_paragraph,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        first_line_indent=False,
    )

    math_paragraph = OxmlElement(
        "m:oMathPara"
    )

    math_object = OxmlElement(
        "m:oMath"
    )

    for element in equation_elements:

        math_object.append(
            element
        )

    math_paragraph.append(
        math_object
    )

    equation_paragraph._element.append(
        math_paragraph
    )


    # ============================================================
    # NUMBER CELL
    # ============================================================

    number_cell = table.cell(
        0,
        2,
    )

    number_paragraph = number_cell.paragraphs[0]

    format_paragraph(
        paragraph=number_paragraph,
        alignment=WD_ALIGN_PARAGRAPH.RIGHT,
        first_line_indent=False,
    )

    number_run = number_paragraph.add_run(
        f"({equation_number})"
    )

    set_run_font(
        number_run
    )

    return table


# ================================================================
# SIMPLE EQUATION HELPERS
# ================================================================

def add_simple_equation(
    document,
    text,
    equation_number=None,
):
    """
    Add simple native Word equation.
    """

    return add_equation(
        document=document,
        equation_elements=create_math_text(
            text
        ),
        equation_number=equation_number,
    )


def add_fraction_equation(
    document,
    left_text,
    numerator,
    denominator,
    equation_number=None,
):
    """
    Add equation:

        left_text = numerator / denominator
    """

    equation_elements = [
        create_math_text(
            left_text
        ),
        create_math_text(
            "="
        ),
        create_fraction(
            numerator=numerator,
            denominator=denominator,
        ),
    ]

    return add_equation(
        document=document,
        equation_elements=equation_elements,
        equation_number=equation_number,
    )


# ================================================================
# DOCUMENT STYLES
# ================================================================

def configure_document_styles(
    document,
):
    """
    Configure default Word document styles.
    """

    normal_style = document.styles[
        "Normal"
    ]

    normal_style.font.name = FONT_NAME

    normal_style.font.size = Pt(
        FONT_SIZE_PT
    )

    normal_style_element = normal_style._element

    normal_style_properties = (
        normal_style_element.get_or_add_rPr()
    )

    normal_style_fonts = (
        normal_style_properties.rFonts
    )

    if normal_style_fonts is None:

        normal_style_fonts = OxmlElement(
            "w:rFonts"
        )

        normal_style_properties.insert(
            0,
            normal_style_fonts,
        )

    normal_style_fonts.set(
        qn("w:ascii"),
        FONT_NAME,
    )

    normal_style_fonts.set(
        qn("w:hAnsi"),
        FONT_NAME,
    )

    normal_style_fonts.set(
        qn("w:eastAsia"),
        FONT_NAME,
    )

    normal_style_fonts.set(
        qn("w:cs"),
        FONT_NAME,
    )


# ================================================================
# DOCUMENT PAGE SETTINGS
# ================================================================

def configure_page_settings(
    document,
):
    """
    Configure document page margins.

    A4 page:

        left   = 3.0 cm
        right  = 1.5 cm
        top    = 2.0 cm
        bottom = 2.0 cm
    """

    section = document.sections[0]

    section.left_margin = Cm(
        3.0
    )

    section.right_margin = Cm(
        1.5
    )

    section.top_margin = Cm(
        2.0
    )

    section.bottom_margin = Cm(
        2.0
    )


# ================================================================
# NUMBER FORMAT
# ================================================================

def format_number(
    value,
    digits=3,
):
    """
    Format a number using decimal comma.
    """

    formatted = f"{value:.{digits}f}"

    return formatted.replace(
        ".",
        ",",
    )


def format_integer(
    value,
):
    """
    Format integer engineering value.
    """

    return f"{value:.0f}"


# ================================================================
# SECTION 01 REPORT
# ================================================================

def create_section01_word_report(
    result,
    P2,
    U1,
    poles,
    protection,
    f1,
    output_path=None,
):
    """
    Create Word report for Section 1.

    Parameters
    ----------
    result : dict
        Final Section 1 calculation result.

    P2 : float
        Rated output power, kW.

    U1 : float
        Rated line voltage, V.

    poles : int
        Number of poles 2p.

    protection : str
        Protection degree.

    f1 : float
        Supply frequency, Hz.

    output_path : str or Path, optional
        Custom DOCX path.

    Returns
    -------
    pathlib.Path
        Created report path.
    """


    # ============================================================
    # OUTPUT PATH
    # ============================================================

    if output_path is None:

        REPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            REPORT_DIRECTORY
            / REPORT_FILENAME
        )

    else:

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


    # ============================================================
    # DOCUMENT
    # ============================================================

    document = Document()

    configure_document_styles(
        document
    )

    configure_page_settings(
        document
    )


    # ============================================================
    # SECTION TITLE
    # ============================================================

    add_section_title(
        document=document,
        text="1 ВЫБОР ГЛАВНЫХ РАЗМЕРОВ",
    )


    # ============================================================
    # INITIAL DATA
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Главные размеры асинхронного двигателя "
            "выбираем в соответствии с методикой "
            "проектирования электрических машин. "
            "Исходными данными для расчета являются "
            f"номинальная полезная мощность P₂ = "
            f"{format_number(P2, 2)} кВт, номинальное "
            f"линейное напряжение U₁ = "
            f"{format_integer(U1)} В, число полюсов "
            f"2p = {poles}, степень защиты "
            f"{protection} и частота питающей сети "
            f"f₁ = {format_number(f1, 1)} Гц."
        ),
    )


    # ============================================================
    # P01 - SHAFT HEIGHT
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Высоту оси вращения асинхронного двигателя "
            "выбираем в зависимости от номинальной мощности, "
            "числа полюсов и степени защиты двигателя по "
            "рис. 9.18."
        ),
    )

    add_text_paragraph(
        document=document,
        text=(
            f"Для двигателя мощностью P₂ = "
            f"{format_number(P2, 2)} кВт, с числом полюсов "
            f"2p = {poles} и степенью защиты "
            f"{protection} принимаем высоту оси вращения:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"h={format_integer(result['h'])} мм"
        ),
    )


    # ============================================================
    # P02 - OUTER STATOR DIAMETER
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "По принятой высоте оси вращения определяем "
            "наружный диаметр сердечника статора. "
            f"Для h = {format_integer(result['h'])} мм "
            "рекомендуемый диапазон наружного диаметра "
            "сердечника статора составляет "
            f"Dₐ = {format_number(result['Da_min'], 3)}..."
            f"{format_number(result['Da_max'], 3)} м. "
            "Принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"Dₐ={format_number(result['Da'], 3)} м"
        ),
    )


    # ============================================================
    # P03 - INNER DIAMETER COEFFICIENT
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Коэффициент отношения внутреннего диаметра "
            "сердечника статора к его наружному диаметру "
            "выбираем в зависимости от числа полюсов. "
            f"При 2p = {poles} рекомендуемый диапазон "
            f"составляет K_D = "
            f"{format_number(result['Kd_min'], 2)}..."
            f"{format_number(result['Kd_max'], 2)}. "
            "Принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"K_D={format_number(result['Kd'], 2)}"
        ),
    )

    add_text_paragraph(
        document=document,
        text=(
            "Внутренний диаметр сердечника статора "
            "определяем по выражению"
        ),
    )

    add_simple_equation(
        document=document,
        text="D=K_D·Dₐ",
        equation_number="1.1",
    )

    add_text_paragraph(
        document=document,
        text="Подставляя численные значения, получаем",
    )

    add_simple_equation(
        document=document,
        text=(
            f"D={format_number(result['Kd'], 2)}·"
            f"{format_number(result['Da'], 3)}="
            f"{format_number(result['D'], 3)} м"
        ),
    )


    # ============================================================
    # POLE PITCH
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Полюсное деление статора определяем по формуле"
        ),
    )

    add_fraction_equation(
        document=document,
        left_text="τ",
        numerator="πD",
        denominator="2p",
        equation_number="1.2",
    )

    add_text_paragraph(
        document=document,
        text="Подставляя численные значения, получаем",
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "τ="
            ),
            create_fraction(
                numerator=(
                    f"π·{format_number(result['D'], 3)}"
                ),
                denominator=(
                    f"{poles}"
                ),
            ),
            create_math_text(
                f"={format_number(result['tau'], 3)} м"
            ),
        ],
    )


    # ============================================================
    # P04 - KE
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Коэффициент отношения ЭДС обмотки статора "
            "к номинальному напряжению выбираем по "
            "соответствующей расчетной зависимости. "
            "Принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"K_E={format_number(result['Ke'], 3)}"
        ),
    )


    # ============================================================
    # P05 - ETA
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Предварительное значение коэффициента полезного "
            "действия двигателя выбираем в зависимости от "
            "номинальной мощности, числа полюсов и степени "
            "защиты:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"η={format_number(result['eta'], 3)}"
        ),
    )


    # ============================================================
    # P06 - COS PHI
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Предварительное значение коэффициента мощности "
            "двигателя принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"cosφ={format_number(result['cos_phi'], 3)}"
        ),
    )


    # ============================================================
    # CALCULATED POWER
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Расчетную мощность электрической машины "
            "определяем по выражению"
        ),
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "P′="
            ),
            create_fraction(
                numerator="P₂K_E",
                denominator="ηcosφ",
            ),
        ],
        equation_number="1.3",
    )

    add_text_paragraph(
        document=document,
        text="Подставляя численные значения, получаем",
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "P′="
            ),
            create_fraction(
                numerator=(
                    f"{format_number(P2, 2)}·1000·"
                    f"{format_number(result['Ke'], 3)}"
                ),
                denominator=(
                    f"{format_number(result['eta'], 3)}·"
                    f"{format_number(result['cos_phi'], 3)}"
                ),
            ),
            create_math_text(
                f"={format_integer(result['P_prime'])} ВА"
            ),
        ],
    )


    # ============================================================
    # P07 - B DELTA
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Предварительное значение магнитной индукции "
            "в воздушном зазоре выбираем по рекомендуемому "
            "диапазону. Для рассматриваемого двигателя "
            f"B_δ = {format_number(result['B_delta_min'], 3)}..."
            f"{format_number(result['B_delta_max'], 3)} Тл. "
            "Принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"B_δ={format_number(result['B_delta'], 3)} Тл"
        ),
    )


    # ============================================================
    # P08 - LINEAR CURRENT LOADING
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Предварительное значение линейной токовой "
            "нагрузки выбираем по рекомендуемому диапазону "
            "для принятого наружного диаметра сердечника "
            "статора. Рекомендуемый диапазон составляет "
            f"A = {format_integer(result['A_min'])}..."
            f"{format_integer(result['A_max'])} А/м. "
            "Принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"A={format_integer(result['A'])} А/м"
        ),
    )


    # ============================================================
    # ALPHA DELTA
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Коэффициент формы кривой распределения магнитной "
            "индукции в воздушном зазоре предварительно "
            "принимаем равным"
        ),
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "α_δ="
            ),
            create_fraction(
                numerator="2",
                denominator="π",
            ),
            create_math_text(
                f"={format_number(result['alpha_delta'], 3)}"
            ),
        ],
    )


    # ============================================================
    # KB
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Коэффициент формы магнитного поля определяем "
            "по выражению"
        ),
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "k_B="
            ),
            create_fraction(
                numerator="π",
                denominator="2√2",
            ),
            create_math_text(
                f"={format_number(result['k_B'], 3)}"
            ),
        ],
    )


    # ============================================================
    # WINDING FACTOR
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Предварительное значение обмоточного коэффициента "
            "обмотки статора принимаем:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"k_об1={format_number(result['kw1'], 3)}"
        ),
    )


    # ============================================================
    # SYNCHRONOUS SPEED
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Синхронная частота вращения магнитного поля "
            "статора составляет:"
        ),
    )

    add_simple_equation(
        document=document,
        text=(
            f"n₁={format_integer(result['n1_rpm'])} об/мин"
        ),
    )


    # ============================================================
    # OMEGA
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Синхронную угловую частоту вращения магнитного "
            "поля определяем по формуле"
        ),
    )

    add_fraction_equation(
        document=document,
        left_text="Ω",
        numerator="2πf₁",
        denominator="p",
        equation_number="1.4",
    )

    pole_pairs = poles / 2

    add_text_paragraph(
        document=document,
        text="Подставляя численные значения, получаем",
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "Ω="
            ),
            create_fraction(
                numerator=(
                    f"2π·{format_number(f1, 1)}"
                ),
                denominator=(
                    f"{format_number(pole_pairs, 0)}"
                ),
            ),
            create_math_text(
                f"={format_number(result['Omega'], 3)} рад/с"
            ),
        ],
    )


    # ============================================================
    # CORE LENGTH
    # KOPYLOV FORMULA 9.6
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Расчетную длину магнитопровода статора определяем "
            "по формуле"
        ),
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "l_δ="
            ),
            create_fraction(
                numerator="P′",
                denominator=(
                    "D²Ωk_Bk_об1AB_δ"
                ),
            ),
        ],
        equation_number="1.5",
    )

    add_text_paragraph(
        document=document,
        text=(
            "Подставляя полученные значения параметров, "
            "определяем расчетную длину магнитопровода:"
        ),
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "l_δ="
            ),
            create_fraction(
                numerator=(
                    f"{format_integer(result['P_prime'])}"
                ),
                denominator=(
                    f"{format_number(result['D'], 4)}²·"
                    f"{format_number(result['Omega'], 3)}·"
                    f"{format_number(result['k_B'], 4)}·"
                    f"{format_number(result['kw1'], 3)}·"
                    f"{format_integer(result['A'])}·"
                    f"{format_number(result['B_delta'], 3)}"
                ),
            ),
            create_math_text(
                f"={format_number(result['l_delta'], 4)} м"
            ),
        ],
    )


    # ============================================================
    # P09 - LAMBDA CHECK
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Правильность выбора главных размеров двигателя "
            "проверяем по отношению расчетной длины "
            "магнитопровода к полюсному делению:"
        ),
    )

    add_fraction_equation(
        document=document,
        left_text="λ",
        numerator="l_δ",
        denominator="τ",
        equation_number="1.6",
    )

    add_text_paragraph(
        document=document,
        text="Для проектируемого двигателя получаем",
    )

    add_equation(
        document=document,
        equation_elements=[
            create_math_text(
                "λ="
            ),
            create_fraction(
                numerator=(
                    f"{format_number(result['l_delta'], 4)}"
                ),
                denominator=(
                    f"{format_number(result['tau'], 4)}"
                ),
            ),
            create_math_text(
                f"={format_number(result['lambda'], 3)}"
            ),
        ],
    )


    # ============================================================
    # LAMBDA CONCLUSION
    # ============================================================

    add_text_paragraph(
        document=document,
        text=(
            "Согласно рекомендациям методики проектирования "
            f"допустимый диапазон отношения λ для выбранного "
            f"исполнения двигателя составляет "
            f"{format_number(result['lambda_min'], 3)}..."
            f"{format_number(result['lambda_max'], 3)}."
        ),
    )

    if result["status"] == "PERMISSIBLE":

        add_text_paragraph(
            document=document,
            text=(
                f"Полученное значение λ = "
                f"{format_number(result['lambda'], 3)} "
                "находится в допустимом диапазоне. "
                "Следовательно, выбранные главные размеры "
                "асинхронного двигателя удовлетворяют "
                "рекомендациям методики проектирования."
            ),
        )

    else:

        add_text_paragraph(
            document=document,
            text=(
                f"Полученное значение λ = "
                f"{format_number(result['lambda'], 3)} "
                "не находится в допустимом диапазоне. "
                "Выбранные главные размеры требуют "
                "дополнительной корректировки."
            ),
        )


    # ============================================================
    # SAVE DOCUMENT
    # ============================================================

    document.save(
        output_path
    )

    return output_path


# ================================================================
# MODULE INFORMATION
# ================================================================

if __name__ == "__main__":

    print(
        "DEE Section 01 Word Report Generator"
    )

    print(
        "This module must be called from main.py "
        "with the final Section 1 calculation result."
    )