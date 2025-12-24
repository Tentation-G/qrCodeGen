from pathlib import Path
import pandas as pd
from rich.text import Text

from textual.app import App, ComposeResult
from textual.theme import Theme
from textual.widgets import Static, DirectoryTree, DataTable, Header, Footer, OptionList, Button, Input
from textual.containers import Container, Vertical

from app.utils import format_loading_bar
from app import main
couple_dict = main.xlsx_to_res_des(file_path="app/data_samples/ExcelParsingSample.xlsx")

# -------------------- File Explorer -------------------- #
class FileExplorer(DirectoryTree):
    DEFAULT_CLASSES = "box-item"
    BORDER_TITLE = "File Explorer"

    ICON_FILE = "{f} "
    ICON_DIR = "[D] "
    ICON_DIR_OPEN = "[D} "

    def render_label(self, node, base_style, style):
        # node.label = nom "nu" (sans icône) dans beaucoup de versions
        name = node.label.plain if hasattr(node.label, "plain") else str(node.label)

        path = node.data.path
        if path.is_dir():
            icon = self.ICON_DIR_OPEN if node.is_expanded else self.ICON_DIR
        else:
            icon = self.ICON_FILE

        return Text(icon + name, style=style)
"""
class FileExplorer(ComposeResult):
    #DEFAULT_CLASSES = "box-item"
    BORDER_TITLE = "File Explorer"

    def compose(self) -> ComposeResult:
        yield DirectoryTree("/")
"""
# ------------------------------------------------------- #

# -------------------- Sheets Tables -------------------- #
def load_excel(path: Path) -> pd.DataFrame:
    return pd.read_excel(path).fillna("")

class SheetsTables(Container):
    BORDER_TITLE = "Data Tables"
    def compose(self) -> ComposeResult:
        yield DataTable(id="excel_table")

    def on_mount(self):

        df = load_excel(Path("app/data_samples/ExcelParsingSample.xlsx"))

        table = self.query_one(DataTable)
        table.add_columns(*df.columns.astype(str))

        for row in df.itertuples(index=False):
            table.add_row(*map(str, row))
# ------------------------------------------------------- #

# --------------------- Logs Panel ---------------------- #
class LogsPanel(Container):
    BORDER_TITLE = "Logs"
    DEFAULT_CLASSES = "box-item"
    def compose(self) -> ComposeResult:
        yield Static("Logs", id="logs")
# ------------------------------------------------------- #

class LoadingBar(Container):
    BORDER_TITLE = "Loading Bar"
    DEFAULT_CLASSES = "box-item"

    def compose(self) -> ComposeResult:
        yield Static("", id="loading_text")

    def on_mount(self) -> None:
        self.current = 0
        self.total = 0

        self.call_after_refresh(self.render_bar)

    def on_resize(self) -> None:
        self.render_bar()

    def bar_width(self) -> int:
        width = self.content_size.width
        return max(1, int(width - 28))

    def render_bar(self) -> None:
        width = self.bar_width()
        text = format_loading_bar(self.current, self.total, barLength=width)
        self.query_one("#loading_text", Static).update(text)

# -------------------- Main - Content ------------------- #
class Content(Container):
    BORDER_TITLE = "Content Section"
    DEFAULT_CLASSES = "box-item"

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Chemin du fichier Excel :", classes="label")
            yield Input(placeholder="app/data_samples/file.xlxs", id="input_file")

            yield Static("Chemin de sortie :", classes="label")
            yield Input(placeholder="app/_pdfOut/", id="input_output")

"""
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Input(placeholder="Chemin d'acces fichier")
            yield Input(placeholder="Chemin de sortie fichier")
"""
# ------------------------------------------------------- #

# ------------------------ Main ------------------------- #
class Main(Container):
    def compose(self) -> ComposeResult:
        with Container(id="sidebar-wrapper"):
            yield FileExplorer("/")

            file_select = Static("", classes="box-item")
            file_select.border_title = "File Selection"
            yield file_select

        with Container(id="content-wrapper"):
            with Container(id="section1"):
                yield Content()

                yield LogsPanel()

            with Container(id="section2"):
                yield LoadingBar()

                file_picker = Static("", id="File-Picker", classes="box-item")
                file_picker.border_title = "File-Picker"
                yield file_picker


            yield SheetsTables()
# ------------------------------------------------------- #

# ------------------------- App ------------------------- #
class LayoutQrCodeGen(App):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("ctrl+q", "quit", "Quitter l'application"),
        ("ctrl+t", "change_theme", "Changer de theme"),

        ("ctrl+f", "focus_input_file", "Focus Input I"),
        ("ctrl+o", "focus_output_file", "Focus Input O"),
    ]

    def on_key(self, event):
        if event.key == "escape" and isinstance(self.focused, Input):
            self.set_focus(None)

    def action_focus_input_file(self) -> None:
        self.query_one("#input_file", Input).focus()

    def action_focus_output_file(self) -> None:
        self.query_one("#input_output", Input).focus()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_path = ""
        self.output_path = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Main()
        yield Footer()
    def on_mount(self) -> None:
        self.title = "qrCodeGen"
        self.sub_title = "Alpha 0.1"

        self.register_theme(wilo_corp_theme)

        #self.theme = "WiloCorporate"
        self.theme = "dracula"
# ------------------------------------------------------- #

wilo_corp_theme = Theme(
    name="WiloCorporate",
    # Couleurs "brand"
    primary="#009C82",    # WiloGreen (R0 G156 B130)
    secondary="#005ACD",  # WaterBlue (R0 G90 B205)
    accent="#FFB400",     # TechniCYellow (R255 G180 B0)

    # Lisibilité / base
    foreground="#FFFFFF", # ClearWhite
    background="#202020", # GunMetal-Mod (R32 G32 B32)

    # États
    success="#AAC800",    # NaturalGreen (R170 G200 B0)
    warning="#FFB400",    # TechniCYellow
    error="#F54100",      # VitalRed (R245 G65 B0)

    # Surfaces UI (cartes/panels)
    surface="#787878",    # CoolGrey (R120 G120 B120)
    panel="#202020",      # GunMetal (cohérent en dark)

    dark=True,
    variables={
        # Confort de lecture / interactions
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#FFB400",          # TechniCYellow
        "input-selection-background": "#005ACD 35%", # WaterBlue à 35%
        "link-color": "#005ACD",                     # liens
        "warning-text": "#FFB400",
        "error-text": "#F54100",
        "success-text": "#AAC800",
    },
)

if __name__ == "__main__":
    LayoutQrCodeGen().run()

