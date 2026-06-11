from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Image, Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
import pandas as pd
import os

# ── Dimensões ────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

# ── Paleta Looqbox ───────────────────────────────────────────
DARK    = colors.HexColor("#3D3D3D")   # cinza escuro ("box")
GREEN   = colors.HexColor("#00E676")   # verde neon principal
GREEN2  = colors.HexColor("#00C15A")   # verde secundário (subsections)
ZEBRA   = colors.HexColor("#F0FDF4")   # fundo zebra tabelas
GRAY    = colors.HexColor("#5A5A5A")   # texto corpo
GRIDCOL = colors.HexColor("#D1D5DB")   # linhas da tabela
WHITE   = colors.white
BLACK   = colors.HexColor("#1A1A1A")

# ── Estilos ───────────────────────────────────────────────────
_base = getSampleStyleSheet()

def _s(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=_base[parent], **kw)

S = {
    "cover_name":  _s("cover_name",  fontSize=28, textColor=DARK,
                       leading=32, spaceAfter=2, fontName="Helvetica-Bold"),
    "cover_sub":   _s("cover_sub",   fontSize=13, textColor=GREEN2,
                       leading=16, spaceAfter=0),
    "cover_meta":  _s("cover_meta",  fontSize=9,  textColor=GRAY, leading=13),
    "cover_note":  _s("cover_note",  fontSize=7.5, textColor=GRAY,
                       leading=11, spaceBefore=8),
    "subsection":  _s("subsection",  fontSize=10, textColor=GREEN2,
                       leading=13, spaceBefore=6, spaceAfter=2,
                       fontName="Helvetica-Bold"),
    "body":        _s("body",        fontSize=8.5, textColor=GRAY,
                       leading=12, spaceBefore=0, spaceAfter=4),
    "code":        _s("code", "Code", fontSize=7.2, leading=10, leftIndent=8,
                       backColor=colors.HexColor("#F3F4F6"),
                       borderColor=GRIDCOL, borderWidth=0.5,
                       borderPad=6, spaceBefore=3, spaceAfter=6),
    "caption":     _s("caption",     fontSize=7.5, textColor=GRAY,
                       leading=10, alignment=TA_CENTER, spaceAfter=4),
}


# ── Helpers ───────────────────────────────────────────────────

def section_header(title: str) -> list:
    """Barra escura Looqbox com título da seção."""
    return [
        Spacer(1, 8),
        Table(
            [[Paragraph(f"<b>{title}</b>",
               _s(f"sh_{title}", fontSize=11, textColor=WHITE, leading=14))]],
            colWidths=[CONTENT_W],
            style=TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), DARK),
                ("TOPPADDING",    (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ("LEFTPADDING",   (0,0), (-1,-1), 10),
                ("LINEBELOW",     (0,0), (-1,-1), 2, GREEN),
            ]),
        ),
        Spacer(1, 6),
    ]


def df_to_table(df: pd.DataFrame, col_widths=None) -> Table:
    """Converte DataFrame em Table ReportLab formatada."""
    header = list(df.columns)
    rows   = [header] + [list(r) for r in df.itertuples(index=False)]

    if col_widths is None:
        col_widths = [CONTENT_W / len(header)] * len(header)

    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  7.5),
        ("TOPPADDING",    (0,0), (-1,0),  5),
        ("BOTTOMPADDING", (0,0), (-1,0),  5),
        ("LINEBELOW",     (0,0), (-1,0),  1.5, GREEN),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 7.2),
        ("TOPPADDING",    (0,1), (-1,-1), 3),
        ("BOTTOMPADDING", (0,1), (-1,-1), 3),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, ZEBRA]),
        ("GRID",          (0,0), (-1,-1), 0.3, GRIDCOL),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl


def scaled_image(path: str, width: float, caption: str = None) -> list:
    """Carrega imagem mantendo proporção original."""
    if not os.path.exists(path):
        return []
    try:
        from PIL import Image as PILImg
        with PILImg.open(path) as im:
            w, h = im.size
            height = width * (h / w)
    except Exception:
        height = width * 0.6
    elems = [Image(path, width=width, height=height)]
    if caption:
        elems.append(Paragraph(caption, S["caption"]))
    return elems


def logo_image(logo_path: str, width: float = 5 * cm) -> list:
    """Carrega a logo removendo fundo preto e escalando."""
    if not os.path.exists(logo_path):
        return []
    try:
        from PIL import Image as PILImg
        import io, tempfile
        with PILImg.open(logo_path) as im:
            im = im.convert("RGBA")
            data = im.getdata()
            # Torna pixels pretos/muito escuros transparentes
            new_data = []
            for r, g, b, a in data:
                if r < 40 and g < 40 and b < 40:
                    new_data.append((0, 0, 0, 0))
                else:
                    new_data.append((r, g, b, a))
            im.putdata(new_data)
            w, h = im.size
            height = width * (h / w)
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            im.save(tmp.name, "PNG")
            tmp_path = tmp.name
        return [Image(tmp_path, width=width, height=height)]
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════

def build_pdf(
    sql_test_result: dict,
    case1_result:    pd.DataFrame,
    case2_result:    pd.DataFrame,
    case3_result,
    output: str = "outputs/looqbox_report.pdf",
    logo_path: str = "logo.png",
):
    """
    Gera o PDF consolidado do desafio Looqbox.

    Parâmetros
    ----------
    sql_test_result : dict  com chaves 'query_1', 'query_2', 'query_3' (DataFrames)
    case1_result    : DataFrame retornado por retrieve_data()
    case2_result    : DataFrame com colunas Loja / Categoria / TM
    case3_result    : qualquer valor (gráficos já salvos em outputs/)
    output          : caminho do PDF gerado
    logo_path       : caminho para logo.png (relativo à raiz do projeto)
    """
    os.makedirs(Path(output).parent, exist_ok=True)

    doc = SimpleDocTemplate(
        output, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=MARGIN,
    )
    E = []

    # ╔══════════════════════════════════╗
    # ║            CAPA                 ║
    # ╚══════════════════════════════════╝
    E.append(Spacer(1, 1.5 * cm))

    # Logo centralizada
    logo_elems = logo_image(logo_path, width=6 * cm)
    if logo_elems:
        logo_row = Table(
            [logo_elems],
            colWidths=[CONTENT_W],
            style=TableStyle([("ALIGN", (0,0), (-1,-1), "LEFT")]),
        )
        E.append(logo_row)
        E.append(Spacer(1, 0.6 * cm))

    E += [
        HRFlowable(width="100%", thickness=3, color=GREEN, spaceAfter=10),
        Paragraph("Data Challenge", S["cover_name"]),
        Paragraph("Relatório Técnico", S["cover_sub"]),
        Spacer(1, 0.4 * cm),
        HRFlowable(width="100%", thickness=0.5, color=GRIDCOL, spaceAfter=8),
        Paragraph("Candidato: <b>João Barbosa</b>", S["cover_meta"]),
        Paragraph("Stack: Python · MySQL · pandas · matplotlib · seaborn · reportlab",
                  S["cover_meta"]),
        Paragraph(
            "<i>Nota de transparência: Claude (Anthropic) foi utilizado como apoio "
            "pontual na estruturação do código de compilação looqbox_challenge.py, generate_report.py, "
            "auxílios de sintaxe e boas práticas nos cases e escolha de bibliotecas de "
            "visualização e de geração d. A lógica SQL, o raciocínio analítico, estruturação dos diretórios, arquivos e as adaptações "
            "ao banco de dados foram realizados pelo candidato.</i>",
            S["cover_note"],
        ),
        PageBreak(),
    ]

    # ╔══════════════════════════════════╗
    # ║          SQL TEST               ║
    # ╚══════════════════════════════════╝
    E += section_header("SQL Test")

    # Q1
    q1_df = sql_test_result.get("query_1", pd.DataFrame())
    E.append(Paragraph("<b>Q1 — 10 produtos mais caros</b>", S["subsection"]))
    E.append(Paragraph(
        "Ordenação decrescente por <code>PRODUCT_VAL</code> com <code>LIMIT 10</code>.",
        S["body"]))
    E.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "SELECT PRODUCT_COD, PRODUCT_NAME, PRODUCT_VAL<br/>"
        "FROM data_product<br/>"
        "ORDER BY PRODUCT_VAL DESC LIMIT 10;"
        "</font>", S["code"]))
    if not q1_df.empty:
        E.append(df_to_table(q1_df, col_widths=[2.5*cm, 10.5*cm, 2.5*cm]))
    E.append(Spacer(1, 8))

    # Q2
    q2_df = sql_test_result.get("query_2", pd.DataFrame())
    E.append(Paragraph("<b>Q2 — Seções de BEBIDAS e PADARIA</b>", S["subsection"]))
    E.append(Paragraph(
        "<code>DISTINCT</code> em <code>SECTION_NAME</code> com "
        "<code>WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')</code>.",
        S["body"]))
    E.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "SELECT DISTINCT DEP_NAME, SECTION_NAME, SECTION_COD<br/>"
        "FROM data_product<br/>"
        "WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')<br/>"
        "ORDER BY DEP_NAME, SECTION_NAME;"
        "</font>", S["code"]))
    if not q2_df.empty:
        E.append(df_to_table(q2_df, col_widths=[4*cm, 8*cm, 3.5*cm]))
    E.append(Spacer(1, 8))

    # Q3
    q3_df = sql_test_result.get("query_3", pd.DataFrame())
    E.append(Paragraph("<b>Q3 — Vendas por Business Area (Q1 2019)</b>", S["subsection"]))
    E.append(Paragraph(
        "JOIN entre <code>data_product_sales</code> e <code>data_store_cad</code>, "
        "filtrando <code>DATE BETWEEN '2019-01-01' AND '2019-03-31'</code>, "
        "agrupado por <code>BUSINESS_NAME</code>.",
        S["body"]))
    E.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "SELECT sc.BUSINESS_NAME, ROUND(SUM(ps.SALES_VALUE), 2) AS Total_Vendas<br/>"
        "FROM data_product_sales ps<br/>"
        "JOIN data_store_cad sc ON ps.STORE_CODE = sc.STORE_CODE<br/>"
        "WHERE ps.DATE BETWEEN '2019-01-01' AND '2019-03-31'<br/>"
        "GROUP BY sc.BUSINESS_NAME ORDER BY Total_Vendas DESC;"
        "</font>", S["code"]))
    if not q3_df.empty:
        E.append(df_to_table(q3_df, col_widths=[8*cm, 7.5*cm]))

    E.append(PageBreak())

    # ╔══════════════════════════════════╗
    # ║          CASE 1                 ║
    # ╚══════════════════════════════════╝
    E += section_header("Case 1 — Função retrieve_data")
    E.append(Paragraph(
        "Função dinâmica que constrói a cláusula <code>WHERE</code> apenas com os "
        "filtros fornecidos. Todos os parâmetros são <b>opcionais</b>, tornando a "
        "função reutilizável por qualquer equipe. O uso de parâmetros "
        "parametrizados (<code>%s</code>) evita SQL injection.",
        S["body"]))
    E.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "def retrieve_data(<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;product_code: Optional[int] = None,<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;store_code:   Optional[int] = None,<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;date:         Optional[list] = None,<br/>"
        ") -> pd.DataFrame:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;conditions, params = [], []<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if product_code: conditions.append('PRODUCT_CODE = %s')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if store_code:   conditions.append('STORE_CODE = %s')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if date:         conditions.append('DATE BETWEEN %s AND %s')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;where = 'WHERE ' + ' AND '.join(conditions) if conditions else ''<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;sql = f'SELECT * FROM data_product_sales {where};'<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return pd.read_sql(sql, get_connection(), params=params or None)"
        "</font>", S["code"]))
    E.append(Paragraph("<b>Exemplos de uso</b>", S["subsection"]))
    E.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "retrieve_data()  # sem filtros — retorna tudo<br/>"
        "retrieve_data(product_code=301409)<br/>"
        "retrieve_data(store_code=3, date=['2019-01-01', '2019-03-31'])"
        "</font>", S["code"]))
    if not case1_result.empty:
        E.append(Paragraph("<b>Resultado (primeiras linhas)</b>", S["subsection"]))
        E.append(df_to_table(case1_result.head(10)))
    else:
        E.append(Paragraph(
            "Nenhum registro encontrado para os filtros de exemplo utilizados.",
            S["body"]))

    E.append(PageBreak())

    # ╔══════════════════════════════════╗
    # ║          CASE 2                 ║
    # ╚══════════════════════════════════╝
    E += section_header("Case 2 — Ticket Médio por Loja (Q4 2019)")
    E.append(Paragraph(
        "As duas queries do cliente foram usadas <b>sem modificação</b>. "
        "O filtro de período <code>['2019-10-01', '2019-12-31']</code> foi aplicado "
        "em Python após o carregamento. O Ticket Médio foi calculado como "
        "<code>SALES_VALUE / SALES_QTY</code> por loja, seguido de JOIN com os dados cadastrais.",
        S["body"]))
    if not case2_result.empty:
        E.append(df_to_table(case2_result, col_widths=[5.5*cm, 5.5*cm, 4.5*cm]))
    E += scaled_image(
        "outputs/case2_ticket_medio.png", width=15*cm,
        caption="Figura 1 — Ticket Médio por Loja, Q4 2019 (out–dez). Cores por categoria.",
    )

    E.append(PageBreak())

    # ╔══════════════════════════════════╗
    # ║          CASE 3                 ║
    # ╚══════════════════════════════════╝
    E += section_header("Case 3 — Análise IMDB")
    E.append(Paragraph("<b>Visualização 1: Violin Plot — notas por década</b>", S["subsection"]))
    E.append(Paragraph(
        "O violin plot foi preferido ao bar chart de médias porque revela a "
        "<b>distribuição completa</b> das notas. Décadas antigas concentram notas "
        "mais altas por viés de sobrevivência: apenas os filmes mais marcantes "
        "permanecem bem avaliados ao longo do tempo — padrão invisível em barras simples.",
        S["body"]))
    E += scaled_image(
        "outputs/case3_imdb_violinplot.png", width=15*cm,
        caption="Figura 2 — Distribuição das notas IMDB por década de lançamento.",
    )
    E.append(Spacer(1, 6))
    E.append(Paragraph("<b>Visualização 2: Top 10 gêneros por nota média</b>", S["subsection"]))
    E.append(Paragraph(
        "Bar chart horizontal dos gêneros com maior nota média "
        "(mínimo de 20 filmes para excluir gêneros com amostra insuficiente).",
        S["body"]))
    E += scaled_image(
        "outputs/case3_imdb_genre.png", width=14*cm,
        caption="Figura 3 — Top 10 gêneros por nota média IMDB (mín. 20 filmes).",
    )

    doc.build(E)
    print(f"✅ PDF gerado: {output}")