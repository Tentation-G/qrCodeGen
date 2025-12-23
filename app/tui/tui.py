from pathlib import Path
import pandas as pd
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree, DataTable, Header, Footer, OptionList, Button
from textual.containers import Container, Horizontal, Vertical

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
        return max(1, int(width - 26))

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
            yield OptionList(id="columns_list")
            yield Button("Default", id="btn_default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        main.qrCode_lib_grid_pdf_gen(couple_dict, dispo=1, need_output=False, )

    def on_mount(self) -> None:
        option_list = self.query_one("#columns_list", OptionList)

        df = getattr(self.app, "df", None)
        if df is None:
            option_list.add_option("Aucune donnée")
            return

        for col in df.columns:
            option_list.add_option(str(col))
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
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Main()
        yield Footer()
    def on_mount(self) -> None:
        self.title = "qrCodeGen"
        self.sub_title = "Alpha 0.1"
# ------------------------------------------------------- #

if __name__ == "__main__":
    LayoutQrCodeGen().run()

