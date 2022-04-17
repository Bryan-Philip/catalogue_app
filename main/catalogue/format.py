from openpyxl import cell
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, NamedStyle

def readExcel():
    return

font = Font(
    name='Arial Nova Light',
    size=11,
    bold=False,
    italic=False,
    vertAlign=None,
    underline='none',
    strike=False,
    color='FF000000'
)
fill = PatternFill(
    fill_type=None,
    start_color='FFFFFFFF',
    end_color='FF000000'
)
border = Border(
    left=Side(border_style=None,
                color='FF000000'),
    right=Side(border_style=None,
                color='FF000000'),
    top=Side(border_style=None,
                color='FF000000'),
    bottom=Side(border_style=None,
                color='FF000000'),
    diagonal=Side(border_style=None,
                    color='FF000000'),
    diagonal_direction=0,
    outline=Side(border_style=None,
                    color='FF000000'),
    vertical=Side(border_style=None,
                    color='FF000000'),
    horizontal=Side(border_style=None,
                    color='FF000000')
)
alignment=Alignment(
    horizontal='general',
    vertical='bottom',
    text_rotation=0,
    wrap_text=False,
    shrink_to_fit=False,
    indent=0
)
number_format = 'General'
protection = Protection(
    locked=True,
    hidden=False
)

FORMAT_INITIAL = NamedStyle(
    name="initial",
    font= Font(
        name="Arial"
    ),
    number_format="center"
)

FORMAT_CENTER = NamedStyle(
    name="centerhv",
    alignment = Alignment(
        horizontal='center',
        vertical='center'
    )
)

FORMAT_CENTER_GENERAL = NamedStyle(
    name="centerhg",
    alignment = Alignment(
        horizontal='center',
        vertical='center'
    ),
    font=Font(
        size=11,
        bold=False
    ),
)

FORMAT_TITLE = NamedStyle(
    name="title",
    font=Font(
        size=22,
        bold=True
    ),
    alignment = Alignment(
        horizontal='center',
        vertical='center'
    ),
)

FORMAT_SUBTITLE = NamedStyle(
    name="subtitle",
    font=Font(
        size=18,
        bold=True
    ),
    alignment = Alignment(
        horizontal='center',
        vertical='center'
    ),
)

class Format:
    def fontSize(cell: cell, fontsize: float):
        cell.font += Font(size=fontsize)
    def GeneralCenter(cell: cell):
        cell.style = FORMAT_CENTER_GENERAL
    def formatTitle(cell: cell):
        cell.style = FORMAT_TITLE
    def formatSubTitle(cell: cell):
        cell.style = FORMAT_SUBTITLE


# ft = Font(color="FF0000")
# a1 = sheet['A3']
# a1.font = ft

# print(a1.value)

# a1.font = Font(color="FF0000", italic=True)

# wb.close()
# wb.save('populated.xlsx')